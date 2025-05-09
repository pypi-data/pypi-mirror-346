import jax.numpy as jnp
from jaxfmm import *
from jax import random

### TODO:
# - check if the FMM error scaling roughly works out

def test_potential_unitcube():
    N = 2**15
    key = random.key(856)
    pts = random.uniform(key,(N,3))
    chrgs = random.uniform(key,N,minval=-1,maxval=1)

    tree_info = gen_hierarchy(pts)
    pot_FMM = eval_potential(**tree_info,chrgs=chrgs)

    pot_dir = eval_potential_direct(pts,chrgs)

    err = jnp.linalg.norm(pot_dir-pot_FMM)/jnp.linalg.norm(pot_dir)
    assert err < 3.75e-3

def test_field_unitcube():
    N = 2**15
    key = random.key(856)
    pts = random.uniform(key,(N,3))
    chrgs = random.uniform(key,N,minval=-1,maxval=1)

    tree_info = gen_hierarchy(pts)
    field_FMM = eval_potential(**tree_info,chrgs=chrgs,field=True)

    field_dir = eval_potential_direct(pts,chrgs,field=True)

    err = jnp.linalg.norm(field_dir-field_FMM)/jnp.linalg.norm(field_dir)
    assert err < 5.75e-3