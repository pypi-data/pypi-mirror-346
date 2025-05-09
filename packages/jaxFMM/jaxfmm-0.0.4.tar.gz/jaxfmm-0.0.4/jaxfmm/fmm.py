import jax
import jax.numpy as jnp
from functools import partial
from math import log2, ceil, sqrt

__all__ = ["gen_hierarchy", "eval_potential", "eval_potential_direct"]

def get_max_l(N_tot, N_max, n_split = 3): # need to get this outside of the jit compiled function - if the particle number changes too much, we must recompile...
    r"""
    Compute number of levels in the hierarchy.

    :param N_tot: Total number of point charges.
    :type N_tot: int
    :param N_max: Maximum allowed number of point charges per box.
    :type N_max: int
    :param n_split: How many splits per level and box will be performed. Each box will have 2^n_split children.
    :type n_split: int, optional

    :return: The maximum level in the hierarchy.
    :rtype: int
    """
    max_l = int(ceil(log2(N_tot/N_max)/n_split))
    return 0 if max_l < 0 else max_l

@partial(jax.jit, static_argnames = ["max_l", "n_split"])
def balanced_tree(pts, max_l, n_split = 3):
    r"""
    Generate a balanced 2^n-tree hierarchy.

    :param pts: Array of shape (N_tot,3) containing the positions of N_tot point charges.
    :type pts: jnp.array
    :param max_l: Maximum level, computed with get_max_l().
    :type max_l: int
    :param n_split: How many splits per level and box will be performed. Each box will have 2^n_split children.
    :type n_split: int, optional

    :return: Indices to resort pts into the highest level of the hierarchy (includes padding), indices to reverse sorting, centers of the boxes on all levels, sidelengths of the boxes on all levels.
    :rtype: (jnp.array, jnp.array, list(jnp.array), list(jnp.array))
    """
    n_chi = 2**n_split
    idcs = jnp.arange(pts.shape[0], dtype = jnp.int32)[None,:]

    for l in range(max_l*n_split):    # carry out n_split splits on max_l levels in total (we cannot make this a for_i loop as the shape constantly changes)
        splitpos = idcs.shape[1]//2   # split position in the middle
        needpad = idcs.shape[1]%2     # modulo tells us if padding must be inserted

        pts_sorted = pts.at[idcs].get(mode="fill",fill_value=-jnp.nan**2)  # padded values get converted to NaNs - NOTE: due to the argpartition implementation, we need to make sure that all the NaNs have the same sign
        axis_to_split = jnp.argmax(jnp.nanmax(pts_sorted,axis=1) - jnp.nanmin(pts_sorted,axis=1),axis=1)    # nanmax and -min to ignore NaNs
        idcs = idcs[jnp.arange(idcs.shape[0], dtype = jnp.int32)[:,None],jnp.argpartition(pts_sorted[jnp.arange(axis_to_split.shape[0], dtype = jnp.int32),:,axis_to_split],splitpos,axis=1)] # splitting - the NaNs introduced below get transported to the beginning

        # padding so the next array has the correct shape - this does not break JIT compiling because it can be computed from only the input shape
        idcs = jax.lax.pad(idcs,jnp.int32(pts.shape[0]),[(0,0,0),(0,needpad,0)])   # pad at the end with out of range values
        idcs = idcs.reshape((-1,idcs.shape[1]//2))                      # now that we padded, we can safely reshape this
    
    idcs = jnp.sort(idcs,axis=1)    # sorting is good for locality but might be overkill TODO: swap only first and last positions instead of full sort?
    rev_idcs = jnp.argsort(idcs.flatten())[:pts.shape[0]]     # reverse sorting indices, to undo the sorting
    pts_sorted = pts.at[idcs].get(mode="fill",fill_value=jnp.nan)  
    boxcenters, boxlens = [jnp.zeros((n_chi**l,3)) for l in range(max_l+1)], [jnp.zeros((n_chi**l,3)) for l in range(max_l+1)]

    for l in range(max_l,0,-1):
        minc, maxc = jnp.nanmin(pts_sorted,axis=1), jnp.nanmax(pts_sorted,axis=1)    # nanmax and -min to ignore NaNs
        boxlens[l] = maxc - minc    # TODO: in principle we only need to save the norm of this, but it is nice to have for visualizations
        boxcenters[l] = minc + boxlens[l]/2
        pts_sorted = pts_sorted.reshape((-1,pts_sorted.shape[1]*n_chi,3))

    minc, maxc = jnp.nanmin(pts_sorted,axis=1), jnp.nanmax(pts_sorted,axis=1)
    boxlens[0] = maxc - minc             # box sidelengths
    boxcenters[0] = minc + boxlens[0]/2  # box center
    return idcs, rev_idcs, boxcenters, boxlens

#@partial(jax.jit, static_argnames = ["theta", "n_split"])
def gen_connectivity(boxcenters, boxlens, theta = 0.75, n_split = 3): # TODO: is there a way to make this JIT compilable?
    r"""
    Compute connectivity information for a given hierarchy. To determine well-separatedness, we check for

    R + theta * r <= theta * d

    where R = max(r1,r2), r = min(r1,r2) and d is the distance between the centers of two boxes with radii r1 and r2. This should give a FMM error that scales as

    theta^(p+1)
    
    with the expansion order p.

    :param boxcenters: List of boxcenters computed with balanced_tree().
    :type boxcenters: list(jnp.array)
    :param boxlens: List of box sidelengths computed with balanced_tree().
    :type boxlens: list(jnp.array)
    :param theta: Well-separatedness parameter, determines accuracy.
    :type theta: float
    :param n_split: How many splits per level and box have been performed. Each box has 2^n_split children.
    :type n_split: int, optional

    :return: List of (padded) M2L interaction partner index arrays for each box on each level, array of (padded) P2P interaction partner indices on the highest level.
    :rtype: (list(jnp.array), jnp.array)
    """
    n_l = len(boxcenters)  # number of levels
    n_chi = 2**n_split     # number of child boxes per split

    mpl_cnct = []
    non_wellseps = jnp.array([[0]], dtype = jnp.int32)     # initial value

    for l in range(n_l):   # for every level
        r1 = jnp.linalg.norm(boxlens[l],axis=1)/2   # L/2 is the radius of the box TODO: see comment on only storing the norm above
        d = jnp.linalg.norm(boxcenters[l][:,None,:] - boxcenters[l].at[non_wellseps].get(mode="fill",fill_value=jnp.nan),axis=-1)  # find the distances between boxcenters
        R = r1[non_wellseps]    # r2
        r = R.copy()
        tmp = (r1[:,None] > R)
        R = jnp.where(tmp,R,r1[:,None])     # wherever r2 < r1, we replace r2 with r1 => R = max(r1,r2)
        r = jnp.where(~tmp,r,r1[:,None])    # wherever r2 > r1, we replace r2 with r1 => r = min(r1,r2)

        wellsep = (R + theta*r <= theta*d)      # NOTE: NaNs always return false here - this is how we rid ourselves of the padding
        non_wellsep = (R + theta*r > theta*d)
        wellsep_nums = wellsep.sum(axis=1, dtype = jnp.int32)          # number of well-separated boxes for each box
        non_wellsep_nums = non_wellsep.sum(axis=1, dtype = jnp.int32)  # number of non-well-separated boxes for each box
        
        to_pad_wellsep = jnp.max(wellsep_nums) - wellsep_nums    # how much padding per box must be inserted
        wellsep_padding = jnp.repeat(jnp.cumsum(wellsep_nums),to_pad_wellsep)   # the correct indices for the insert below NOTE: this has a dynamic size and therefore breaks JIT compilation
        mpl_cnct.append(jnp.insert(non_wellseps[wellsep],wellsep_padding,n_chi**l).reshape(n_chi**l,-1))    # save result to the interaction lists

        to_pad_non_wellsep = jnp.max(non_wellsep_nums) - non_wellsep_nums    # how much padding per box must be inserted for non-well-separated boxes
        non_wellsep_padding = jnp.repeat(jnp.cumsum(non_wellsep_nums),to_pad_non_wellsep)   # the correct indices for the insert below
        non_wellseps = jnp.insert(non_wellseps[non_wellsep],non_wellsep_padding,n_chi**l).reshape((n_chi**l,-1))    # we overwrite the old values here

        if(l<n_l-1):    # prepare for the computation on the next level by transforming to child indices
            non_wellseps = jnp.repeat(jnp.repeat(non_wellseps,n_chi,axis=1)*n_chi + jnp.tile(jnp.arange(n_chi, dtype = jnp.int32),non_wellseps.shape[1]),n_chi,axis=0)

    return mpl_cnct, non_wellseps

def mpl_idx(m,n):
    r"""
    Compute "flattened" array position of multipole coefficient C^m_n with order m and degree n.
    """
    return n**2 + (m+n)

def inv_mpl_idx(idx):
    r"""
    Compute order m and degree n of "flattened" array position idx.
    """
    n = int(sqrt(idx))
    m = idx - n*(n+1)
    return m, n

@partial(jax.jit, static_argnames=['p'])
def eval_regular_basis(rvec, p):
    r"""
    Evaluate real regular basis functions (Laplace kernel) with a recursion relation [Gumerov, N. A. et al. Fast multipole methods on graphics processors. J. Comp. Phys., B 227, 8290 (2008)].

    :param rvec: Array of positions in cartesian coordinates to evaluate the basis at.
    :type rvec: jnp.array
    :param p: Maximum degree (degree of multipole expansion) for the evaluation.
    :type p: int

    :return: Regular basis evaluated until the given degree at the given locations.
    :rtype: jnp.array
    """
    x, y, z = rvec[..., 0], rvec[...,1], rvec[...,2]
    coeff = jnp.zeros((*rvec.shape[:-1], (p+1)**2))
    coeff = coeff.at[...,mpl_idx(0,0)].set(1)

    if(p>0):
        coeff = coeff.at[...,mpl_idx(1,1)].set(-0.5*x)
        coeff = coeff.at[...,mpl_idx(-1,1)].set(0.5*y)

    for n in range(2,p+1):    # first recursion: extreme values
        coeff = coeff.at[...,mpl_idx(n,n)].set(-(x*coeff[...,mpl_idx(n-1,n-1)] + y*coeff[...,mpl_idx(1-n,n-1)])/(2*n))
        coeff = coeff.at[...,mpl_idx(-n,n)].set((y*coeff[...,mpl_idx(n-1,n-1)] - x*coeff[...,mpl_idx(1-n,n-1)])/(2*n))

    for n in range(0,p):      # second recursion: neighbors of extreme values
        coeff = coeff.at[...,mpl_idx(n,n+1)].set(-z*coeff[...,mpl_idx(n,n)])
        coeff = coeff.at[...,mpl_idx(-n,n+1)].set(-z*coeff[...,mpl_idx(-n,n)])

    for n in range(2,p+1):    # third recursion: all values inbetween
        for m in range(-n+2,n-1):
            coeff = coeff.at[...,mpl_idx(m,n)].set(-((2*n-1)*z*coeff[...,mpl_idx(m,n-1)] + (x**2+y**2+z**2)*coeff[...,mpl_idx(m,n-2)])/((n-abs(m))*(n+abs(m))))
    
    return coeff

@partial(jax.jit, static_argnames=['p'])
def eval_regular_basis_grad(rvec, p):
    r"""
    Evaluate the gradient of real regular basis functions (Laplace kernel) with a recursion relation.

    :param rvec: Array of positions in cartesian coordinates to evaluate the basis at.
    :type rvec: jnp.array
    :param p: Maximum degree (degree of multipole expansion) for the evaluation.
    :type p: int

    :return: Gradient of the regular basis evaluated until the given degree at the given locations.
    :rtype: jnp.array
    """
    scal_coeff = eval_regular_basis(rvec, p)

    x, y, z = rvec[..., 0], rvec[...,1], rvec[...,2]
    coeff = jnp.zeros((*rvec.shape[:-1], (p+1)**2, 3))

    if(p>0):
        coeff = coeff.at[...,mpl_idx(1,1),0].set(-0.5)
        coeff = coeff.at[...,mpl_idx(-1,1),1].set(0.5)

    for n in range(2,p+1):    # first recursion: extreme values
        coeff = coeff.at[...,mpl_idx(n,n),:].set(x[...,None]*coeff[...,mpl_idx(n-1,n-1),:] + y[...,None]*coeff[...,mpl_idx(1-n,n-1),:])
        coeff = coeff.at[...,mpl_idx(n,n),0].add(scal_coeff[...,mpl_idx(n-1,n-1)])
        coeff = coeff.at[...,mpl_idx(n,n),1].add(scal_coeff[...,mpl_idx(1-n,n-1)])
        coeff = coeff.at[...,mpl_idx(n,n),:].divide(-2*n)

        coeff = coeff.at[...,mpl_idx(-n,n),:].set(y[...,None]*coeff[...,mpl_idx(n-1,n-1),:] - x[...,None]*coeff[...,mpl_idx(1-n,n-1),:])
        coeff = coeff.at[...,mpl_idx(-n,n),0].subtract(scal_coeff[...,mpl_idx(1-n,n-1)])
        coeff = coeff.at[...,mpl_idx(-n,n),1].add(scal_coeff[...,mpl_idx(n-1,n-1)])
        coeff = coeff.at[...,mpl_idx(-n,n),:].divide(2*n)

    for n in range(0,p):      # second recursion: neighbors of extreme values
        coeff = coeff.at[...,mpl_idx(n,n+1),:].set(-z[...,None]*coeff[...,mpl_idx(n,n),:])
        coeff = coeff.at[...,mpl_idx(n,n+1),2].subtract(scal_coeff[...,mpl_idx(n,n)])

        coeff = coeff.at[...,mpl_idx(-n,n+1),:].set(-z[...,None]*coeff[...,mpl_idx(-n,n),:])
        coeff = coeff.at[...,mpl_idx(-n,n+1),2].subtract(scal_coeff[...,mpl_idx(-n,n)])

    for n in range(2,p+1):    # third recursion: all values inbetween
        for m in range(-n+2,n-1):
            coeff = coeff.at[...,mpl_idx(m,n),:].set((2*n-1)*z[...,None]*coeff[...,mpl_idx(m,n-1),:] + (x**2+y**2+z**2)[...,None]*coeff[...,mpl_idx(m,n-2),:] + 2*scal_coeff[...,mpl_idx(m,n-1),None]*rvec)
            coeff = coeff.at[...,mpl_idx(m,n),2].add((2*n - 1) * scal_coeff[...,mpl_idx(m,n-1)])
            coeff = coeff.at[...,mpl_idx(m,n),:].divide((abs(m) - n) * (n + abs(m)))

    return coeff

@partial(jax.jit, static_argnames=['p'])
def eval_singular_basis(rvec, p):   # NOTE: might have to include a factor (-1)^n, also use S_n^-m for evaluating
    r"""
    Evaluate real singular basis functions (Laplace kernel) with a recursion relation.

    :param rvec: Array of positions in cartesian coordinates to evaluate the basis at.
    :type rvec: jnp.array
    :param p: Maximum degree (degree of multipole expansion) for the evaluation.
    :type p: int

    :return: Singular basis evaluated until the given degree at the given locations.
    :rtype: jnp.array
    """
    x, y, z = rvec[..., 0], rvec[...,1], rvec[...,2]
    r2 = x**2 + y**2 + z**2
    coeff = jnp.zeros((*rvec.shape[:-1], (p+1)**2))
    coeff = coeff.at[...,mpl_idx(0,0)].set(1/jnp.sqrt(r2))

    if(p>0):
        coeff = coeff.at[...,mpl_idx(1,1)].set(-coeff[...,mpl_idx(0,0)]*y/r2)
        coeff = coeff.at[...,mpl_idx(-1,1)].set(coeff[...,mpl_idx(0,0)]*x/r2)

    for n in range(2,p+1):    # first recursion: extreme values
        coeff = coeff.at[...,mpl_idx(n,n)].set((2*n-1)*(x*coeff[...,mpl_idx(n-1,n-1)] - y*coeff[...,mpl_idx(1-n,n-1)])/r2)
        coeff = coeff.at[...,mpl_idx(-n,n)].set((2*n-1)*(y*coeff[...,mpl_idx(n-1,n-1)] + x*coeff[...,mpl_idx(1-n,n-1)])/r2)

    for n in range(0,p):      # second recursion: neighbors of extreme values
        coeff = coeff.at[...,mpl_idx(n,n+1)].set((2*n+1)*z*coeff[...,mpl_idx(n,n)]/r2)
        coeff = coeff.at[...,mpl_idx(-n,n+1)].set((2*n+1)*z*coeff[...,mpl_idx(-n,n)]/r2)

    for n in range(2,p+1):    # third recursion: all values inbetween
        for m in range(-n+2,n-1):
            coeff = coeff.at[...,mpl_idx(m,n)].set(((2*n-1)*z*coeff[...,mpl_idx(m,n-1)] - (n-1-m)*(n-1+m)*coeff[...,mpl_idx(m,n-2)])/r2)
    
    return coeff

@partial(jax.jit, static_argnames=['p'])
def get_initial_mpls(padded_pts, padded_chrgs, boxcenters, p):
    r"""
    Get initial multipole expansions for each box on the highest level.

    :param padded_pts: Array of point positions, sorted into the highest level of the hierarchy via balanced_tree().
    :type padded_pts: jnp.array
    :param padded_chrgs: Array of point charges, sorted into the highest level of the hierarchy via balanced_tree().
    :type padded_chrgs: jnp.array
    :param boxcenters: Array of box centers, generated via balanced_tree().
    :type boxcenters: jnp.array
    :param p: Multipole expansion order.
    :type p: int

    :return: Array of multipole coefficients of the boxes on the highest level.
    :rtype: jnp.array
    """
    dist = padded_pts - boxcenters[:,None]
    return (eval_regular_basis(dist,p) * padded_chrgs[...,None]).sum(axis=1)

@partial(jax.jit, static_argnames=['p', 'n_split'])
def M2M(coeff, oldboxdims, newboxdims, p, n_split):
    r"""
    Multipole-to-multipole transformation, merging "small" multipole expansions on higher levels into "large" multipole expansions on lower levels. This is the O(p^4) algorithm proposed in the original 3D FMM paper.

    :param coeff: Array of multipole coefficients on level l.
    :type coeff: jnp.array
    :param oldboxdims: Array of box centers on level l.
    :type oldboxdims: jnp.array
    :param newboxdims: Array of box centers on level l-1.
    :type newboxdims: jnp.array
    :param p: Multipole expansion order.
    :type p: int
    :param n_split: How many splits per level and box have been performed. Each box has 2^n_split children which are merged into one in this function.
    :type n_split: int

    :return: Array of multipole coefficients of the boxes on level l-1.
    :rtype: jnp.array
    """
    n_chi = 2**n_split
    mpls = coeff.reshape((coeff.shape[0]//n_chi,n_chi,coeff.shape[1]))
    new_mpls = jnp.zeros((mpls.shape[0],mpls.shape[2]))
    oldboxdims = oldboxdims.reshape((-1,n_chi,3))
    reg = eval_regular_basis(oldboxdims - newboxdims[:,None,:],p)   # shift direction points from target to source

    for j in range(p+1):
        for k in range(0,j+1):  # Real coeffs
            for n in range(j+1):
                for m in range(max(k+n-j,-n),min(k+j-n,n)+1):
                    new_mpls = new_mpls.at[...,mpl_idx(k,j)].set(new_mpls[...,mpl_idx(k,j)] + (-1)**((abs(k)-abs(m)-abs(k-m))//2) * (
                                                  reg[...,mpl_idx(abs(m),n)]*mpls[...,mpl_idx(abs(k-m),j-n)] - 
                                                  jnp.sign(m)*jnp.sign(k-m)*reg[...,mpl_idx(-abs(m),n)]*mpls[...,mpl_idx(-abs(k-m),j-n)]).sum(axis=-1))
        for k in range(-j,0):   # Imag coeffs
            for n in range(j+1):
                for m in range(max(k+n-j,-n),min(k+j-n,n)+1):
                    new_mpls = new_mpls.at[...,mpl_idx(k,j)].set( new_mpls[...,mpl_idx(k,j)] - (-1)**((abs(k)-abs(m)-abs(k-m))//2) * (
                                                  jnp.sign(k-m)*reg[...,mpl_idx(abs(m),n)]*mpls[...,mpl_idx(-abs(k-m),j-n)] + 
                                                  jnp.sign(m)*reg[...,mpl_idx(-abs(m),n)]*mpls[...,mpl_idx(abs(k-m),j-n)]).sum(axis=-1))
    return new_mpls

@partial(jax.jit, static_argnames=['p', 'n_split'])
def L2L(locs, oldboxdims, newboxdims, p, n_split):
    r"""
    Local-to-local transformation, distributing "large" local expansions on lower levels to "small" local expansions on higher levels. This is the O(p^4) algorithm proposed in the original 3D FMM paper.

    :param locs: Array of local coefficients on level l.
    :type locs: jnp.array
    :param oldboxdims: Array of box centers on level l.
    :type oldboxdims: jnp.array
    :param newboxdims: Array of box centers on level l+1.
    :type newboxdims: jnp.array
    :param p: Multipole expansion order.
    :type p: int
    :param n_split: How many splits per level and box have been performed. Each box has 2^n_split children which all receive a local expansion of their parent in this function.
    :type n_split: int

    :return: Array of local coefficients of the boxes on level l+1.
    :rtype: jnp.array
    """
    n_chi = 2**n_split
    new_locs = jnp.zeros((locs.shape[0], n_chi, locs.shape[1]))
    newboxdims = newboxdims.reshape((-1,n_chi,3))
    reg = eval_regular_basis(oldboxdims[:,None,:]-newboxdims,p)   # shift direction points from target to source

    for j in range(p+1):
        for k in range(1,j+1):  # -Imag coeffs!
            for n in range(j,p+1):
                for m in range(k+j-n,k+n-j+1):
                    new_locs = new_locs.at[...,mpl_idx(k,j)].set(new_locs[...,mpl_idx(k,j)] - (-1)**((abs(m)-abs(m-k)-abs(k))//2) * (
                                                  -jnp.sign(m)*reg[...,mpl_idx(abs(m-k),n-j)]*locs[...,None,mpl_idx(abs(m),n)] + 
                                                  jnp.sign(m-k)*reg[...,mpl_idx(-abs(m-k),n-j)]*locs[...,None,mpl_idx(-abs(m),n)]))
        for k in range(-j,1):   # Real coeffs!
            for n in range(j,p+1):
                for m in range(k+j-n,k+n-j+1):
                    new_locs = new_locs.at[...,mpl_idx(k,j)].set(new_locs[...,mpl_idx(k,j)] + (-1)**((abs(m)-abs(m-k)-abs(k))//2) * (
                                                  reg[...,mpl_idx(abs(m-k),n-j)]*locs[...,None,mpl_idx(-abs(m),n)] + 
                                                  jnp.sign(m-k)*jnp.sign(m)*reg[...,mpl_idx(-abs(m-k),n-j)]*locs[...,None,mpl_idx(abs(m),n)]))
    return new_locs.reshape((-1,new_locs.shape[-1]))

@partial(jax.jit, static_argnames=['p'])
def M2L(mpls, locs, boxcenters, mpl_cnct, p):  # TODO: try to write this as a jax.pallas kernel?
    r"""
    Multipole-to-local transformation, turning multipole expansions into local expansions on the same level. This is the O(p^4) algorithm proposed in the original 3D FMM paper.

    :param mpls: Array of multipole coefficients.
    :type mpls: jnp.array
    :param locs: Array of local coefficients.
    :type locs: jnp.array
    :param boxcenters: Array of box centers.
    :type boxcenters: jnp.array
    :param mpl_cnct: Array containing interaction partner indices for each box.
    :type mpl_cnct: jnp.array
    :param p: Multipole expansion order.
    :type p: int

    :return: Updated array of local coefficients, now includes all the well-separated multipole expansions on this level.
    :rtype: jnp.array
    """
    sing = eval_singular_basis(boxcenters.at[mpl_cnct].get(mode="fill",fill_value=123456789)-boxcenters[:,None,:],p)    # shift direction points from target to source TODO: find a proper way of getting non-nan values here

    for j in range(p+1):
        for k in range(1,j+1):  # -Imag coeffs!
            for n in range(p+1-j):
                for m in range(max(k-j-n,-n),min(j+n+k,n)+1):
                    locs = locs.at[:,mpl_idx(k,j)].set( locs[:,mpl_idx(k,j)] + (-1)**((abs(k-m)-abs(k)-abs(m))//2) * (
                                                -jnp.sign(m-k)*sing[...,mpl_idx(abs(m-k),j+n)]*mpls.at[mpl_cnct,mpl_idx(abs(m),n)].get(mode="fill",fill_value=0) + 
                                                jnp.sign(m)*sing[...,mpl_idx(-abs(m-k),j+n)]*mpls.at[mpl_cnct,mpl_idx(-abs(m),n)].get(mode="fill",fill_value=0)).sum(axis=1))
        for k in range(-j,1):  # Real coeffs!
            for n in range(p+1-j):
                for m in range(max(k-j-n,-n),min(j+n+k,n)+1):
                    locs = locs.at[:,mpl_idx(k,j)].set(locs[:,mpl_idx(k,j)] + (-1)**((abs(k-m)-abs(k)-abs(m))//2) * (
                                                sing[...,mpl_idx(-abs(m-k),j+n)]*mpls.at[mpl_cnct,mpl_idx(abs(m),n)].get(mode="fill",fill_value=0) + 
                                                jnp.sign(m)* jnp.sign(m-k) * sing[...,mpl_idx(abs(m-k),j+n)]*mpls.at[mpl_cnct,mpl_idx(-abs(m),n)].get(mode="fill",fill_value=0)).sum(axis=1))
    return locs

@partial(jax.jit, static_argnames=['p', 'n_split'])
def go_up(coeff, boxcenters, p, n_split):
    r"""
    Using multipole-to-multipole transformation, descend the hierarchy.

    :param coeff: Array of multipole coefficients on the highest level.
    :type coeff: jnp.array
    :param boxcenters: List containing box center arrays for every level.
    :type boxcenters: list(jnp.array)
    :param p: Multipole expansion order.
    :type p: int
    :param n_split: How many splits per level and box have been performed. Each box has 2^n_split children which are merged on every level for this step.
    :type n_split: int

    :return: List of multipole coefficient arrays, containing multipole expansion coefficients for every box on every level.
    :rtype: list(jnp.array)
    """
    mpls = [coeff]
    n_l = len(boxcenters)
    for i in range(n_l-1):
        mpls.append(M2M(mpls[-1],boxcenters[-(i+1)],boxcenters[-(i+2)], p, n_split))
    return mpls

@partial(jax.jit, static_argnames=['p', 'n_split'])
def go_down(mpls, boxcenters, mpl_cnct, p, n_split):
    r"""
    Using multipole-to-local and local-to-local transformation, ascend the hierarchy.

    :param mpls: List of multipole coefficient arrays on every level.
    :type mpls: list(jnp.array)
    :param boxcenters: List containing box center arrays for every level.
    :type boxcenters: list(jnp.array)
    :param mpl_cnct: List of interaction partner index arrays on every level.
    :type mpl_cnct: list(jnp.array)
    :param p: Multipole expansion order.
    :type p: int
    :param n_split: How many splits per level and box have been performed. Each box has 2^n_split children which receive local expansions from their parent in this step.
    :type n_split: int

    :return: List of local coefficient arrays, containing local expansion coefficients for every box on every level.
    :rtype: list(jnp.array)
    """
    locs = [jnp.zeros((mpls[-1].shape))]
    n_l = len(boxcenters)
    for i in range(n_l-1):  # for every level TODO: level 1 can be skipped
        locs.append(L2L(locs[-1],boxcenters[i],boxcenters[i+1], p, n_split)) # get local expansions from parent boxes
        locs[-1] = M2L(mpls[-(i+2)], locs[-1], boxcenters[i+1], mpl_cnct[i+1], p) # next, it is time to do the M2L shifts for this level
    return locs

@partial(jax.jit, static_argnames=['p'])
def eval_local(locs, padded_pts, rev_idcs, boxcenters, p):
    r"""
    Evaluate local expansions on the highest level.

    :param locs: Array of local coefficients on the highest level.
    :type locs: jnp.array
    :param padded_pts: Array containing point positions, sorted into the highest level of the hierarchy.
    :type padded_pts: jnp.array
    :param rev_idcs: Index array to remove padding and return to original sorting.
    :type rev_idcs: jnp.array
    :param boxcenters: Array of box center positions on the highest level.
    :type boxcenters: jnp.array
    :param p: Multipole expansion order.
    :type p: int

    :return: Far-field potential in the original sorting positions.
    :rtype: jnp.array
    """
    padded_res = jnp.zeros(padded_pts.shape[:2])
    reg = eval_regular_basis(padded_pts-boxcenters[:,None],p)   # this evaluation needs to be relative to the boxcenter

    for n in range(p+1):
        for m in range(-n,n+1):
            if(m!=0):
                padded_res += (-1)**n * 2*locs[:,None,mpl_idx(-m,n)] * reg[...,mpl_idx(m,n)]
            else:
                padded_res += (-1)**n * locs[:,None,mpl_idx(-m,n)] * reg[...,mpl_idx(m,n)]
    return padded_res.flatten()[rev_idcs] / (4*jnp.pi)  # TODO: flatten and resort only once, after adding?

@partial(jax.jit, static_argnames=['p'])
def eval_local_field(locs, padded_pts, rev_idcs, boxcenters, p):
    r"""
    Evaluate the negative gradient of the local expansions on the highest level.

    :param locs: Array of local coefficients on the highest level.
    :type locs: jnp.array
    :param padded_pts: Array containing point positions, sorted into the highest level of the hierarchy.
    :type padded_pts: jnp.array
    :param rev_idcs: Index array to remove padding and return to original sorting.
    :type rev_idcs: jnp.array
    :param boxcenters: Array of box center positions on the highest level.
    :type boxcenters: jnp.array
    :param p: Multipole expansion order.
    :type p: int

    :return: Far-field in the original sorting positions.
    :rtype: jnp.array
    """
    padded_res = jnp.zeros(padded_pts.shape[:3])
    reg = eval_regular_basis_grad(padded_pts-boxcenters[:,None], p)

    for n in range(p+1):
        for m in range(-n,n+1):
            if(m!=0):
                padded_res += (-1)**n * 2*locs[:,None,mpl_idx(-m,n),None] * reg[:,:,mpl_idx(m,n),:]
            else:
                padded_res += (-1)**n * locs[:,None,mpl_idx(-m,n),None] * reg[:,:,mpl_idx(m,n),:]
    return -padded_res.reshape((-1,3))[rev_idcs] / (4*jnp.pi)

@jax.jit
def eval_direct(padded_pts, padded_chrgs, rev_idcs, direct_cnct): # TODO: replace some of these evaluations with multipole evaluations for better performance
    r"""
    Evaluate the near-field potential directly (P2P).

    :param padded_pts: Array containing point positions, sorted into the highest level of the hierarchy.
    :type padded_pts: jnp.array
    :param padded_chrgs: Array containing point charges, sorted into the highest level of the hierarchy.
    :type padded_chrgs: jnp.array
    :param rev_idcs: Index array to remove padding and return to original sorting.
    :type rev_idcs: jnp.array
    :param direct_cnct: Index array of interaction partners for each box on the highest level.
    :type direct_cnct: jnp.array

    :return: Near-field potential in the original sorting positions.
    :rtype: jnp.array
    """
    n = padded_pts.shape[1]
    nrows = padded_pts.shape[0]

    def i_body(i):
        acc = jnp.zeros((n,))
        xblk = padded_pts[i]
        def k_body(k, acc):
            partner = direct_cnct[i,k]
            dists = jnp.linalg.norm(xblk[:,None] - padded_pts[partner],axis=-1)
            dists = 1/jnp.where(dists==0,jnp.inf,dists)
            chunk = padded_chrgs.at[partner].get(mode="fill",fill_value=0.0)
            return acc + dists.dot(chunk)
        acc = jax.lax.fori_loop(0,direct_cnct.shape[1], k_body, acc)
        return acc

    accs = jax.vmap(i_body)(jnp.arange(nrows))
    return accs.flatten()[rev_idcs]/(4*jnp.pi) # TODO: flatten and resort only once, after adding?

@jax.jit
def eval_direct_field(padded_pts, padded_chrgs, rev_idcs, direct_cnct):
    r"""
    Evaluate the near-field directly (P2P).

    :param padded_pts: Array containing point positions, sorted into the highest level of the hierarchy.
    :type padded_pts: jnp.array
    :param padded_chrgs: Array containing point charges, sorted into the highest level of the hierarchy.
    :type padded_chrgs: jnp.array
    :param rev_idcs: Index array to remove padding and return to original sorting.
    :type rev_idcs: jnp.array
    :param direct_cnct: Index array of interaction partners for each box on the highest level.
    :type direct_cnct: jnp.array

    :return: Near-field in the original sorting positions.
    :rtype: jnp.array
    """
    n = padded_pts.shape[1]
    nrows = padded_pts.shape[0]

    def i_body(i):
        acc = jnp.zeros((n,3))
        xblk = padded_pts[i]
        def k_body(k, acc):
            partner = direct_cnct[i,k]
            distsvec = xblk[:,None] - padded_pts[partner]
            distsnorm = jnp.linalg.norm(distsvec,axis=-1)
            distsnorm = 1/jnp.where(distsnorm==0,jnp.inf,distsnorm)
            chunk = padded_chrgs.at[partner].get(mode="fill",fill_value=0.0)
            return acc + ((chunk[None,:]*(distsnorm**3))[...,None] * distsvec).sum(axis=1)
        acc = jax.lax.fori_loop(0,direct_cnct.shape[1], k_body, acc)
        return acc

    accs = jax.vmap(i_body)(jnp.arange(nrows))
    return accs.reshape((-1,3))[rev_idcs]/(4*jnp.pi)

def gen_hierarchy(pts, N_max = 128, theta = 0.75, n_split = 3, include_boxlens = False):
    r"""
    Generate the balanced tree and connectivity for the FMM.

    :param pts: Array of shape (N,3) containing the positions of N point charges.
    :type pts: jnp.array
    :param N_max: Maximum allowed number of point charges per box.
    :type N_max: int, optional
    :param theta: Well-separatedness parameter, determines accuracy.
    :type theta: float, optional
    :param n_split: How many splits per level and box are been performed. Each box has 2^n_split children.
    :type n_split: int, optional
    :param include_boxlens: Whether to include the box dimensions in the output or not. This is only useful for debugging, as the box dimensions are not needed in the FMM algorithm.
    :type include_boxlens: bool, optional

    :return: Dictionary containing full hierarchy information.
    :rtype: dict
    """
    max_l = get_max_l(pts.shape[0], N_max, n_split)
    idcs, rev_idcs, boxcenters, boxlens = balanced_tree(pts, max_l, n_split)
    mpl_cnct, dir_cnct = gen_connectivity(boxcenters, boxlens, theta, n_split)

    hierarchy = {"pts": pts,
                 "idcs": idcs,
                 "rev_idcs": rev_idcs,
                 "boxcenters": boxcenters,
                 "mpl_cnct": mpl_cnct,
                 "dir_cnct": dir_cnct,
                 "n_split": n_split,
                 "max_l": max_l
                }
    if(include_boxlens):
        hierarchy["boxlens"] = boxlens
    return hierarchy

@partial(jax.jit, static_argnames=['p', 'n_split', 'field'])
def eval_potential(pts, idcs, rev_idcs, boxcenters, mpl_cnct, dir_cnct, n_split, chrgs, p = 3, field = False, **kwargs):
    r"""
    Full FMM potential evaluation, does not include creation of the hierarchy (see gen_hierarchy, which generates a dict containing the first 7 parameters). Therefore, only chrgs and p can be safely changed without recomputing the hierarchy.

    :param pts: Array containing point positions.
    :type pts: jnp.array
    :param idcs: Index array to sort points/charges into highest level of the hierarchy.
    :type idcs: jnp.array
    :param rev_idcs: Index array to remove padding and return to original sorting.
    :type rev_idcs: jnp.array
    :param boxcenters: List containing box center arrays for every level.
    :type boxcenters: list(jnp.array)
    :param mpl_cnct: List of interaction partner index arrays on every level.
    :type mpl_cnct: list(jnp.array)
    :param dir_cnct: Index array of interaction partners for each box on the highest level.
    :type dir_cnct: jnp.array
    :param n_split: How many splits per level and box have been performed. Each box has 2^n_split children.
    :type n_split: int
    :param chrgs: Array containing point charges.
    :type chrgs: jnp.array
    :param p: Multipole expansion order.
    :type p: int, optional
    :param field: Optionally evaluate the field instead of the potential.
    :type field: bool, optional

    :return: Electrostatic potential (or field) of the points and corresponding charges.
    :rtype: jnp.array
    """
    padded_pts = pts.at[idcs].get(mode="fill",fill_value=0.0)   # TODO: we could buffer this alternatively
    padded_chrgs = chrgs.at[idcs].get(mode="fill",fill_value=0.0)
    coeff = get_initial_mpls(padded_pts, padded_chrgs, boxcenters[-1], p)
    mpls = go_up(coeff, boxcenters, p, n_split)
    locs = go_down(mpls, boxcenters, mpl_cnct, p, n_split)

    if(field):
        return eval_direct_field(padded_pts, padded_chrgs, rev_idcs, dir_cnct) + eval_local_field(locs[-1], padded_pts, rev_idcs, boxcenters[-1], p)
    else:
        return eval_direct(padded_pts, padded_chrgs, rev_idcs, dir_cnct) + eval_local(locs[-1], padded_pts, rev_idcs, boxcenters[-1], p)

@partial(jax.jit, static_argnames=['field'])
def eval_potential_direct(pts, chrgs, eval_pts = None, field = False):
    r"""
    Evaluate the potential directly via pairwise sums.

    :param pts: Array containing point positions.
    :type padded_pts: jnp.array
    :param chrgs: Array containing point charges.
    :type chrgs: jnp.array
    :param eval_pts: Array containing points to evaluate the potential at. Defaults to pts.
    :type eval_pts: jnp.array, optional
    :param field: Optionally evaluate the field (negative gradient) instead of the potential.
    :type field: bool, optional

    :return: Electrostatic potential (or field) of the points and corresponding charges.
    :rtype: jnp.array
    """
    if(eval_pts is None):
        eval_pts = pts
    res = jnp.zeros(eval_pts.shape[:field+1])
    def eval_direct_body(i, val):
        distsvec = pts[:,:] - eval_pts[i,None,:]
        inv_dists = jnp.linalg.norm(distsvec,axis=-1)
        inv_dists = 1/jnp.where(inv_dists==0,jnp.inf,inv_dists) # take out self-interaction
        if(field):
            val = val.at[i].set(-((chrgs * inv_dists**3)[:,None] * distsvec).sum(axis=0))
        else:
            val = val.at[i].set((chrgs * inv_dists).sum())
        return val
    return jax.lax.fori_loop(0,eval_pts.shape[0],eval_direct_body,res)/(4*jnp.pi)