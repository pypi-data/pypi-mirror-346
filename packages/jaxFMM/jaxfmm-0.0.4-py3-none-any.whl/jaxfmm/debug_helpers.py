import jax.numpy as jnp
import jax.scipy as jsp
import jaxfmm.fmm as fmm
from math import isqrt
import numpy as np
import pyvista as pv
import os

__all__ = ["print_stats","gen_hierarchy_vtk","gen_wellsep_vtk"]

def print_stats(pts, idcs, rev_idcs, boxcenters, mpl_cnct, dir_cnct, n_split, **kwargs):
    r"""
    Print some basic information about the hierarchy.
    """
    print("----------------------------------------FMM Hierarchy Stats----------------------------------------")
    print("%i points, %i levels, %i children per box, %i charges per box\n"%(pts.shape[0],len(mpl_cnct)-1, 2**n_split, idcs.shape[1]))
    prefix = ["M2L transformations on", "                      "]
    for i in range(len(mpl_cnct)):
        num_nopad = (mpl_cnct[i]<mpl_cnct[i].shape[0]).sum()
        print("%s level %i (with padding, fraction: %.2f): %i"%(prefix[i>0],i, 1 if num_nopad==0 else mpl_cnct[i].size / num_nopad, mpl_cnct[i].size))
    print("\nDirect interactions on level %i (with padding, fraction: %.2f): %i"%(i,dir_cnct.size / (dir_cnct < dir_cnct.shape[0]).sum(),dir_cnct.size))
    print("\nNear field compression ratio (without padding): %.2e"%((((dir_cnct<dir_cnct.shape[0]).sum()) * idcs.shape[1]**2) / (float(pts.shape[0])**2)))
    memory_usage = idcs.nbytes + rev_idcs.nbytes + dir_cnct.nbytes
    for i in range(len(boxcenters)):
        memory_usage += boxcenters[i].nbytes + mpl_cnct[i].nbytes
        if 'boxlens' in kwargs:
            memory_usage += kwargs.get("boxlens")[i].nbytes
    print("\nTotal memory consumed by the hierarchy: %.2e Bytes"%memory_usage)
    print("Total memory consumed by the points:    %.2e Bytes"%pts.nbytes)
    print("---------------------------------------------------------------------------------------------------")

def make_pyvista_mesh(boxcenters, boxlens):
    pv_shifts = np.array([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]])
    pts = np.zeros((boxcenters.shape[0],8,3))
    for i in range(pv_shifts.shape[0]):
        pts[:,i,:] = boxcenters + boxlens/2 * pv_shifts[i,None,:]
    pts = pts.reshape((-1,3))
    cells = np.arange(pts.shape[0],dtype=np.int32).reshape((-1,8))
    return pv.UnstructuredGrid({pv.CellType.HEXAHEDRON: cells}, pts)

def gen_hierarchy_vtk(boxcenters, boxlens, dir="hierarchy", **kwargs):
    r"""
    Output a series of vtk files showing the FMM hierarchy on every level.
    """
    max_l = len(boxcenters)
    if not os.path.exists(dir):
        os.makedirs(dir)
    for l in range(max_l):
        mesh = make_pyvista_mesh(boxcenters[l],boxlens[l])
        mesh.save("%s/level_%i.vtk"%(dir,l))

def gen_wellsep_vtk(id, boxcenters, boxlens, mpl_cnct, dir_cnct, dir="hierarchy", **kwargs):
    r"""
    Output a vtk file showing all the boxes that are considered for potential calculation, given an id of a box on the highest level.
    """
    if not os.path.exists(dir):
        os.makedirs(dir)
    max_l = len(boxcenters) # NOTE: this is max_l + 1
    n_chi = boxcenters[1].shape[0]
    meshlist = []

    for l in range(1,max_l):    # level 0 cannot be well-separated
        extract = mpl_cnct[l][id//(n_chi**(max_l-l-1))]
        extract = extract[extract<mpl_cnct[l].shape[0]]
        mesh = make_pyvista_mesh(boxcenters[l][extract],boxlens[l][extract])
        mesh.cell_data["level"] = np.ones(mesh.points.shape[0]//8)*l
        meshlist.append(mesh)

    extract = dir_cnct[id]
    extract = extract[extract<dir_cnct.shape[0]]
    mesh = make_pyvista_mesh(boxcenters[-1][extract],boxlens[-1][extract])
    mesh.cell_data["level"] = np.ones(mesh.points.shape[0]//8)*max_l
    mesh.cell_data["level"][extract==id] = max_l + 1
    meshlist.append(mesh)

    mergedmesh = pv.merge(meshlist)
    mergedmesh.save("%s/wellsep_%i.vtk"%(dir,id))

def eval_multipole(coeff, boxcenter, eval_pts):
    r"""
    Evaluate a single multipole expansion.
    """
    p = get_deg(coeff.shape[-1])
    sing = fmm.eval_singular_basis(eval_pts - boxcenter,p)
    res = jnp.zeros(eval_pts.shape[0])
    for n in range(p+1):
        for m in range(-n,n+1):
            if(m!=0):
                res += (-1)**n * 2 * coeff[...,fmm.mpl_idx(m,n)] * sing[...,fmm.mpl_idx(-m,n)]
            else:
                res += (-1)**n * coeff[...,fmm.mpl_idx(m,n)] * sing[...,fmm.mpl_idx(-m,n)] 
    res /= (4*jnp.pi)
    return res

def get_local_expansions(pts, chrgs, exp_centers, p):
    r"""
    Generate local expansions.
    """
    dist = pts[None,...] - exp_centers[:,None,:]
    coeff = (fmm.eval_singular_basis(dist,p) * chrgs[None,:,None]).sum(axis=1)
    return coeff

def binom(x, y):
  return jnp.exp(jsp.special.gammaln(x + 1) - jsp.special.gammaln(y + 1) - jsp.special.gammaln(x - y + 1))

def gen_multipole_dist(m, n, eps = 0.5):
    r"""
    Generate a point charge distribution corresponding to a specific multipole moment (Majic, Matt. (2022). Point charge representations of multipoles. European Journal of Physics. 43. 10.1088/1361-6404/ac578b.)
    """
    if(m == 0):   # axial
        k = jnp.arange(-n, n+1, 2)
        chrgs = (-1)**((n-k)/2) * binom(n, (n-k)/2.0) / (jsp.special.factorial(n) * (2*eps)**n)
        pts = jnp.zeros((k.shape[0],3))
        pts = pts.at[:,2].set(k*eps)
    else:         # (stacked) bracelet
        rotate = m < 0
        m = abs(m)      # we work with the real basis and rotate later
        knum = n-m+1
        jnum = 2*m
        j = jnp.tile(jnp.arange(jnum),knum)
        k = jnp.repeat(jnp.arange(-n+m,n-m+1,2),jnum)
        phi = (j-0.5) * jnp.pi/m if rotate else j * jnp.pi/m
        pts = jnp.array([eps*jnp.cos(phi), eps*jnp.sin(phi), k*eps]).T
        chrgs = 4**(m-1) * jsp.special.factorial(m-1) / ((2*eps)**n * jsp.special.factorial(n-m)) * (-1)**((n-m-k)/2 + j) * binom(n-m,(n-m-k)/2)
    return pts, chrgs

def get_deg(N_coeff):
    r"""
    Get the degree p of a multipole expansion from the number of coefficients.
    """
    return isqrt(N_coeff) - 1