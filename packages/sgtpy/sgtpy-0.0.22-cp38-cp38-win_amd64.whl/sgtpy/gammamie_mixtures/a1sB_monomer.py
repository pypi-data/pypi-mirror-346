from __future__ import division, print_function, absolute_import
import numpy as np
from .B_monomer import B, dB_dxhi00, d2B_dxhi00, d3B_dxhi00
from .B_monomer import dB_dx, dB_dx_dxhi00, dB_dx_dxhi00_dxxhi
from .B_monomer import dB_dx_d2xhi00_dxxhi
from .a1s_monomer import a1s, da1s_dxhi00, d2a1s_dxhi00, d3a1s_dxhi00
from .a1s_monomer import da1s_dx, da1s_dx_dxhi00, da1s_dx_dxhi00_dxxhi
from .a1s_monomer import da1s_dx_d2xhi00_dxxhi


def a1sB(xhi00, xhix, xhix_vec, xm, Ikl, Jkl, cictes, a1vdw, a1vdw_cte):
    a1 = a1s(xhi00, xhix_vec, xm, cictes, a1vdw)
    b = B(xhi00, xhix, xm, Ikl, Jkl, a1vdw_cte)
    return a1 + b


def da1sB_dxhi00(xhi00, xhix, xhix_vec, xm, Ikl, Jkl, cictes, a1vdw, a1vdw_cte,
                 dxhix_dxhi00):
    a1, da1 = da1s_dxhi00(xhi00, xhix_vec, xm, cictes, a1vdw,
                          dxhix_dxhi00)
    b, db = dB_dxhi00(xhi00, xhix, xm, Ikl, Jkl, a1vdw_cte, dxhix_dxhi00)
    return a1 + b, da1 + db


def d2a1sB_dxhi00(xhi00, xhix, xhix_vec, xm, Ikl, Jkl, cictes, a1vdw,
                  a1vdw_cte, dxhix_dxhi00):
    a1, da1, d2a1 = d2a1s_dxhi00(xhi00, xhix_vec, xm, cictes, a1vdw,
                                 dxhix_dxhi00)
    b, db, d2b = d2B_dxhi00(xhi00, xhix, xm, Ikl, Jkl, a1vdw_cte, dxhix_dxhi00)
    return a1 + b, da1 + db, d2a1 + d2b


def d3a1sB_dxhi00(xhi00, xhix, xhix_vec, xm, Ikl, Jkl, cictes, a1vdw,
                  a1vdw_cte, dxhix_dxhi00):
    a1, da1, d2a1, d3a1 = d3a1s_dxhi00(xhi00, xhix_vec, xm, cictes,
                                       a1vdw, dxhix_dxhi00)
    b, db, d2b, d3b = d3B_dxhi00(xhi00, xhix, xm, Ikl, Jkl, a1vdw_cte,
                                 dxhix_dxhi00)
    return a1 + b, da1 + db, d2a1 + d2b, d3a1 + d3b


def da1sB_dx(xhi00, xhix, xhix_vec, xm, ms, Ikl, Jkl, cictes, a1vdw, a1vdw_cte,
             dxhix_dx):
    a1, da1x = da1s_dx(xhi00, xhix_vec, xm, ms, cictes, a1vdw, dxhix_dx)
    b, dbx = dB_dx(xhi00, xhix, xm, ms, Ikl, Jkl, a1vdw_cte,  dxhix_dx)
    return a1 + b, da1x + dbx


def da1sB_dx_dxhi00(xhi00, xhix, xhix_vec, xm, ms, Ikl, Jkl, cictes, a1vdw,
                    a1vdw_cte, dxhix_dxhi00, dxhix_dx):
    a1, da1, da1x = da1s_dx_dxhi00(xhi00, xhix_vec, xm, ms, cictes,
                                   a1vdw, dxhix_dxhi00, dxhix_dx)
    b, db, dbx = dB_dx_dxhi00(xhi00, xhix, xm, ms, Ikl, Jkl, a1vdw_cte,
                              dxhix_dxhi00, dxhix_dx)
    return a1+b, da1+db, da1x+dbx


def da1sB_dx_dxhi00_dxxhi(xhi00, xhix, xhix_vec, xm, ms, Ikl, Jkl, cictes,
                          a1vdw, a1vdw_cte, dxhix_dxhi00, dxhix_dx,
                          dxhix_dx_dxhi00):
    out = da1s_dx_dxhi00_dxxhi(xhi00, xhix_vec, xm, ms, cictes, a1vdw,
                               dxhix_dxhi00, dxhix_dx, dxhix_dx_dxhi00)
    a1, da1, da1x, da1xxhi = out
    out = dB_dx_dxhi00_dxxhi(xhi00, xhix, xm, ms, Ikl, Jkl, a1vdw_cte,
                             dxhix_dxhi00, dxhix_dx, dxhix_dx_dxhi00)
    b, db, dbx, dbxxhi = out
    return a1+b, da1+db, da1x+dbx, da1xxhi+dbxxhi


def da1sB_dx_d2xhi00_dxxhi(xhi00, xhix, xhix_vec, xm, ms, Ikl, Jkl, cictes,
                           a1vdw, a1vdw_cte, dxhix_dxhi00, dxhix_dx,
                           dxhix_dx_dxhi00):
    out = da1s_dx_d2xhi00_dxxhi(xhi00, xhix_vec, xm, ms, cictes, a1vdw,
                                dxhix_dxhi00, dxhix_dx, dxhix_dx_dxhi00)
    a1, da1, d2a1, da1x, da1xxhi = out
    out = dB_dx_d2xhi00_dxxhi(xhi00, xhix, xm, ms, Ikl, Jkl, a1vdw_cte,
                              dxhix_dxhi00, dxhix_dx, dxhix_dx_dxhi00)
    b, db, d2b, dbx, dbxxhi = out
    return a1+b, da1+db, d2a1+d2b, da1x+dbx, da1xxhi+dbxxhi


def a1sB_eval(xhi00, xhix, xhix_vec, xs_m, I_lambdaskl, J_lambdaskl, ccteskl,
              a1vdwkl, a1vdw_ctekl):

    # la_kl, lr_kl, la_kl2, lr_kl2, lar_kl = lambdaskl
    cctes_lakl, cctes_lrkl, cctes_2lakl, cctes_2lrkl, cctes_larkl = ccteskl
    a1vdw_lakl, a1vdw_lrkl, a1vdw_2lakl, a1vdw_2lrkl, a1vdw_larkl = a1vdwkl

    I_lakl, I_lrkl, I_2lakl, I_2lrkl, I_larkl = I_lambdaskl
    J_lakl, J_lrkl, J_2lakl, J_2lrkl, J_larkl = J_lambdaskl

    a1sb_a = a1sB(xhi00, xhix, xhix_vec, xs_m, I_lakl, J_lakl, cctes_lakl,
                  a1vdw_lakl, a1vdw_ctekl)
    a1sb_r = a1sB(xhi00, xhix, xhix_vec, xs_m, I_lrkl, J_lrkl, cctes_lrkl,
                  a1vdw_lrkl, a1vdw_ctekl)
    a1sb_2a = a1sB(xhi00, xhix, xhix_vec, xs_m, I_2lakl, J_2lakl, cctes_2lakl,
                   a1vdw_2lakl, a1vdw_ctekl)
    a1sb_2r = a1sB(xhi00, xhix, xhix_vec, xs_m, I_2lrkl, J_2lrkl, cctes_2lrkl,
                   a1vdw_2lrkl, a1vdw_ctekl)
    a1sb_ar = a1sB(xhi00, xhix, xhix_vec, xs_m, I_larkl, J_larkl, cctes_larkl,
                   a1vdw_larkl, a1vdw_ctekl)

    a1sb_a1 = np.array([a1sb_a, a1sb_r])
    a1sb_a2 = np.array([a1sb_2a, a1sb_ar, a1sb_2r])
    return a1sb_a1, a1sb_a2


def da1sB_dxhi00_eval(xhi00, xhix, xhix_vec, xs_m, I_lambdaskl, J_lambdaskl,
                      ccteskl, a1vdwkl, a1vdw_ctekl, dxhix_dxhi00):

    # la_kl, lr_kl, la_kl2, lr_kl2, lar_kl = lambdaskl
    cctes_lakl, cctes_lrkl, cctes_2lakl, cctes_2lrkl, cctes_larkl = ccteskl
    a1vdw_lakl, a1vdw_lrkl, a1vdw_2lakl, a1vdw_2lrkl, a1vdw_larkl = a1vdwkl

    I_lakl, I_lrkl, I_2lakl, I_2lrkl, I_larkl = I_lambdaskl
    J_lakl, J_lrkl, J_2lakl, J_2lrkl, J_larkl = J_lambdaskl

    a1sb_a, da1sb_a = da1sB_dxhi00(xhi00, xhix, xhix_vec, xs_m, I_lakl, J_lakl,
                                   cctes_lakl, a1vdw_lakl, a1vdw_ctekl,
                                   dxhix_dxhi00)

    a1sb_r, da1sb_r = da1sB_dxhi00(xhi00, xhix, xhix_vec, xs_m, I_lrkl, J_lrkl,
                                   cctes_lrkl, a1vdw_lrkl, a1vdw_ctekl,
                                   dxhix_dxhi00)

    a1sb_2a, da1sb_2a = da1sB_dxhi00(xhi00, xhix, xhix_vec, xs_m, I_2lakl,
                                     J_2lakl, cctes_2lakl, a1vdw_2lakl,
                                     a1vdw_ctekl, dxhix_dxhi00)

    a1sb_2r, da1sb_2r = da1sB_dxhi00(xhi00, xhix, xhix_vec, xs_m, I_2lrkl,
                                     J_2lrkl, cctes_2lrkl, a1vdw_2lrkl,
                                     a1vdw_ctekl, dxhix_dxhi00)

    a1sb_ar, da1sb_ar = da1sB_dxhi00(xhi00, xhix, xhix_vec, xs_m, I_larkl,
                                     J_larkl, cctes_larkl, a1vdw_larkl,
                                     a1vdw_ctekl, dxhix_dxhi00)

    a1sb_a1 = np.array([[a1sb_a, a1sb_r],
                        [da1sb_a, da1sb_r]])
    a1sb_a2 = np.array([[a1sb_2a, a1sb_ar, a1sb_2r],
                       [da1sb_2a, da1sb_ar, da1sb_2r]])

    return a1sb_a1, a1sb_a2


def d2a1sB_dxhi00_eval(xhi00, xhix, xhix_vec, xs_m, I_lambdaskl, J_lambdaskl,
                       ccteskl, a1vdwkl, a1vdw_ctekl, dxhix_dxhi00):

    # la_kl, lr_kl, la_kl2, lr_kl2, lar_kl = lambdaskl
    cctes_lakl, cctes_lrkl, cctes_2lakl, cctes_2lrkl, cctes_larkl = ccteskl
    a1vdw_lakl, a1vdw_lrkl, a1vdw_2lakl, a1vdw_2lrkl, a1vdw_larkl = a1vdwkl

    I_lakl, I_lrkl, I_2lakl, I_2lrkl, I_larkl = I_lambdaskl
    J_lakl, J_lrkl, J_2lakl, J_2lrkl, J_larkl = J_lambdaskl

    out_la = d2a1sB_dxhi00(xhi00, xhix, xhix_vec, xs_m, I_lakl, J_lakl,
                           cctes_lakl, a1vdw_lakl, a1vdw_ctekl, dxhix_dxhi00)
    a1sb_a, da1sb_a, d2a1sb_a = out_la

    out_lr = d2a1sB_dxhi00(xhi00, xhix, xhix_vec, xs_m, I_lrkl, J_lrkl,
                           cctes_lrkl, a1vdw_lrkl, a1vdw_ctekl, dxhix_dxhi00)
    a1sb_r, da1sb_r, d2a1sb_r = out_lr

    out_2la = d2a1sB_dxhi00(xhi00, xhix, xhix_vec, xs_m, I_2lakl, J_2lakl,
                            cctes_2lakl, a1vdw_2lakl, a1vdw_ctekl,
                            dxhix_dxhi00)
    a1sb_2a, da1sb_2a, d2a1sb_2a = out_2la

    out_2lr = d2a1sB_dxhi00(xhi00, xhix, xhix_vec, xs_m, I_2lrkl, J_2lrkl,
                            cctes_2lrkl, a1vdw_2lrkl, a1vdw_ctekl,
                            dxhix_dxhi00)
    a1sb_2r, da1sb_2r, d2a1sb_2r = out_2lr

    out_lar = d2a1sB_dxhi00(xhi00, xhix, xhix_vec, xs_m, I_larkl, J_larkl,
                            cctes_larkl, a1vdw_larkl, a1vdw_ctekl,
                            dxhix_dxhi00)
    a1sb_ar, da1sb_ar, d2a1sb_ar = out_lar

    a1sb_a1 = np.array([[a1sb_a, a1sb_r],
                        [da1sb_a, da1sb_r],
                       [d2a1sb_a, d2a1sb_r]])

    a1sb_a2 = np.array([[a1sb_2a, a1sb_ar, a1sb_2r],
                       [da1sb_2a, da1sb_ar, da1sb_2r],
                       [d2a1sb_2a, d2a1sb_ar, d2a1sb_2r]])
    return a1sb_a1, a1sb_a2


def d3a1sB_dxhi00_eval(xhi00, xhix, xhix_vec, xs_m, I_lambdaskl, J_lambdaskl,
                       ccteskl, a1vdwkl, a1vdw_ctekl, dxhix_dxhi00):

    # la_kl, lr_kl, la_kl2, lr_kl2, lar_kl = lambdaskl
    cctes_lakl, cctes_lrkl, cctes_2lakl, cctes_2lrkl, cctes_larkl = ccteskl
    a1vdw_lakl, a1vdw_lrkl, a1vdw_2lakl, a1vdw_2lrkl, a1vdw_larkl = a1vdwkl

    I_lakl, I_lrkl, I_2lakl, I_2lrkl, I_larkl = I_lambdaskl
    J_lakl, J_lrkl, J_2lakl, J_2lrkl, J_larkl = J_lambdaskl

    out_la = d3a1sB_dxhi00(xhi00, xhix, xhix_vec, xs_m, I_lakl, J_lakl,
                           cctes_lakl, a1vdw_lakl, a1vdw_ctekl, dxhix_dxhi00)
    a1sb_a, da1sb_a, d2a1sb_a, d3a1sb_a = out_la

    out_lr = d3a1sB_dxhi00(xhi00, xhix, xhix_vec, xs_m, I_lrkl, J_lrkl,
                           cctes_lrkl, a1vdw_lrkl, a1vdw_ctekl, dxhix_dxhi00)
    a1sb_r, da1sb_r, d2a1sb_r, d3a1sb_r = out_lr

    out_2la = d3a1sB_dxhi00(xhi00, xhix, xhix_vec, xs_m, I_2lakl, J_2lakl,
                            cctes_2lakl, a1vdw_2lakl, a1vdw_ctekl,
                            dxhix_dxhi00)
    a1sb_2a, da1sb_2a, d2a1sb_2a, d3a1sb_2a = out_2la

    out_2lr = d3a1sB_dxhi00(xhi00, xhix, xhix_vec, xs_m, I_2lrkl, J_2lrkl,
                            cctes_2lrkl, a1vdw_2lrkl, a1vdw_ctekl,
                            dxhix_dxhi00)
    a1sb_2r, da1sb_2r, d2a1sb_2r, d3a1sb_2r = out_2lr

    out_lar = d3a1sB_dxhi00(xhi00, xhix, xhix_vec, xs_m, I_larkl, J_larkl,
                            cctes_larkl, a1vdw_larkl, a1vdw_ctekl,
                            dxhix_dxhi00)
    a1sb_ar, da1sb_ar, d2a1sb_ar, d3a1sb_ar = out_lar

    a1sb_a1 = np.array([[a1sb_a, a1sb_r],
                        [da1sb_a, da1sb_r],
                       [d2a1sb_a, d2a1sb_r],
                       [d3a1sb_a, d3a1sb_r]])

    a1sb_a2 = np.array([[a1sb_2a, a1sb_ar, a1sb_2r],
                       [da1sb_2a, da1sb_ar, da1sb_2r],
                       [d2a1sb_2a, d2a1sb_ar, d2a1sb_2r],
                       [d3a1sb_2a, d3a1sb_ar, d3a1sb_2r]])

    return a1sb_a1, a1sb_a2


def da1sB_dx_eval(xhi00, xhix, xhix_vec, xs_m, zs_m, I_lambdaskl, J_lambdaskl,
                  ccteskl, a1vdwkl, a1vdw_ctekl, dxhix_dx):

    # la_kl, lr_kl, la_kl2, lr_kl2, lar_kl = lambdaskl
    cctes_lakl, cctes_lrkl, cctes_2lakl, cctes_2lrkl, cctes_larkl = ccteskl
    a1vdw_lakl, a1vdw_lrkl, a1vdw_2lakl, a1vdw_2lrkl, a1vdw_larkl = a1vdwkl

    I_lakl, I_lrkl, I_2lakl, I_2lrkl, I_larkl = I_lambdaskl
    J_lakl, J_lrkl, J_2lakl, J_2lrkl, J_larkl = J_lambdaskl

    a1sb_a, da1sb_a = da1sB_dx(xhi00, xhix, xhix_vec, xs_m, zs_m, I_lakl,
                               J_lakl, cctes_lakl, a1vdw_lakl, a1vdw_ctekl,
                               dxhix_dx)
    a1sb_r, da1sb_r = da1sB_dx(xhi00, xhix, xhix_vec, xs_m, zs_m, I_lrkl,
                               J_lrkl, cctes_lrkl, a1vdw_lrkl, a1vdw_ctekl,
                               dxhix_dx)
    a1sb_2a, da1sb_2a = da1sB_dx(xhi00, xhix, xhix_vec, xs_m, zs_m, I_2lakl,
                                 J_2lakl, cctes_2lakl, a1vdw_2lakl,
                                 a1vdw_ctekl, dxhix_dx)
    a1sb_2r, da1sb_2r = da1sB_dx(xhi00, xhix, xhix_vec, xs_m, zs_m, I_2lrkl,
                                 J_2lrkl, cctes_2lrkl, a1vdw_2lrkl,
                                 a1vdw_ctekl, dxhix_dx)
    a1sb_ar, da1sb_ar = da1sB_dx(xhi00, xhix, xhix_vec, xs_m, zs_m, I_larkl,
                                 J_larkl, cctes_larkl, a1vdw_larkl,
                                 a1vdw_ctekl, dxhix_dx)

    a1sb_a1 = np.array([a1sb_a, a1sb_r])
    a1sb_a2 = np.array([a1sb_2a, a1sb_ar, a1sb_2r])

    a1sb_a1x = np.array([da1sb_a, da1sb_r])
    a1sb_a2x = np.array([da1sb_2a, da1sb_ar, da1sb_2r])
    return a1sb_a1, a1sb_a2, a1sb_a1x, a1sb_a2x


def da1sB_dx_dxhi00_eval(xhi00, xhix, xhix_vec, xs_m, zs_m, I_lambdaskl,
                         J_lambdaskl, ccteskl, a1vdwkl, a1vdw_ctekl,
                         dxhix_dxhi00, dxhix_dx):

    # la_kl, lr_kl, la_kl2, lr_kl2, lar_kl = lambdaskl
    cctes_lakl, cctes_lrkl, cctes_2lakl, cctes_2lrkl, cctes_larkl = ccteskl
    a1vdw_lakl, a1vdw_lrkl, a1vdw_2lakl, a1vdw_2lrkl, a1vdw_larkl = a1vdwkl

    I_lakl, I_lrkl, I_2lakl, I_2lrkl, I_larkl = I_lambdaskl
    J_lakl, J_lrkl, J_2lakl, J_2lrkl, J_larkl = J_lambdaskl

    out_la = da1sB_dx_dxhi00(xhi00, xhix, xhix_vec, xs_m, zs_m, I_lakl, J_lakl,
                             cctes_lakl, a1vdw_lakl, a1vdw_ctekl, dxhix_dxhi00,
                             dxhix_dx)
    a1sb_a, da1sb_a, da1sb_ax = out_la
    out_lr = da1sB_dx_dxhi00(xhi00, xhix, xhix_vec, xs_m, zs_m, I_lrkl, J_lrkl,
                             cctes_lrkl, a1vdw_lrkl, a1vdw_ctekl, dxhix_dxhi00,
                             dxhix_dx)
    a1sb_r, da1sb_r, da1sb_rx = out_lr
    out_2la = da1sB_dx_dxhi00(xhi00, xhix, xhix_vec, xs_m, zs_m, I_2lakl,
                              J_2lakl, cctes_2lakl, a1vdw_2lakl, a1vdw_ctekl,
                              dxhix_dxhi00, dxhix_dx)
    a1sb_2a, da1sb_2a, da1sb_2ax = out_2la
    out_2lr = da1sB_dx_dxhi00(xhi00, xhix, xhix_vec, xs_m, zs_m, I_2lrkl,
                              J_2lrkl, cctes_2lrkl, a1vdw_2lrkl, a1vdw_ctekl,
                              dxhix_dxhi00, dxhix_dx)
    a1sb_2r, da1sb_2r, da1sb_2rx = out_2lr
    out_lar = da1sB_dx_dxhi00(xhi00, xhix, xhix_vec, xs_m, zs_m, I_larkl,
                              J_larkl, cctes_larkl, a1vdw_larkl, a1vdw_ctekl,
                              dxhix_dxhi00, dxhix_dx)
    a1sb_ar, da1sb_ar, da1sb_arx = out_lar

    a1sb_a1 = np.array([[a1sb_a, a1sb_r],
                        [da1sb_a, da1sb_r]])
    a1sb_a2 = np.array([[a1sb_2a, a1sb_ar, a1sb_2r],
                       [da1sb_2a, da1sb_ar, da1sb_2r]])

    a1sb_a1x = np.array([da1sb_ax, da1sb_rx])
    a1sb_a2x = np.array([da1sb_2ax, da1sb_arx, da1sb_2rx])

    return a1sb_a1, a1sb_a2, a1sb_a1x, a1sb_a2x


def da1sB_dx_dxhi00_dxxhi_eval(xhi00, xhix, xhix_vec, xs_m, zs_m,
                               I_lambdaskl, J_lambdaskl, ccteskl, a1vdwkl,
                               a1vdw_ctekl, dxhix_dxhi00, dxhix_dx,
                               dxhix_dx_dxhi00):

    # la_kl, lr_kl, la_kl2, lr_kl2, lar_kl = lambdaskl
    cctes_lakl, cctes_lrkl, cctes_2lakl, cctes_2lrkl, cctes_larkl = ccteskl
    a1vdw_lakl, a1vdw_lrkl, a1vdw_2lakl, a1vdw_2lrkl, a1vdw_larkl = a1vdwkl

    I_lakl, I_lrkl, I_2lakl, I_2lrkl, I_larkl = I_lambdaskl
    J_lakl, J_lrkl, J_2lakl, J_2lrkl, J_larkl = J_lambdaskl

    out_la = da1sB_dx_dxhi00_dxxhi(xhi00, xhix, xhix_vec, xs_m, zs_m, I_lakl,
                                   J_lakl, cctes_lakl, a1vdw_lakl, a1vdw_ctekl,
                                   dxhix_dxhi00, dxhix_dx, dxhix_dx_dxhi00)
    a1sb_a, da1sb_a, da1sb_ax, da1sb_axxhi = out_la
    out_lr = da1sB_dx_dxhi00_dxxhi(xhi00, xhix, xhix_vec, xs_m, zs_m, I_lrkl,
                                   J_lrkl, cctes_lrkl, a1vdw_lrkl, a1vdw_ctekl,
                                   dxhix_dxhi00, dxhix_dx, dxhix_dx_dxhi00)
    a1sb_r, da1sb_r, da1sb_rx, da1sb_rxxhi = out_lr
    out_2la = da1sB_dx_dxhi00_dxxhi(xhi00, xhix, xhix_vec, xs_m, zs_m, I_2lakl,
                                    J_2lakl, cctes_2lakl, a1vdw_2lakl,
                                    a1vdw_ctekl, dxhix_dxhi00, dxhix_dx,
                                    dxhix_dx_dxhi00)
    a1sb_2a, da1sb_2a, da1sb_2ax, da1sb_2axxhi = out_2la
    out_2lr = da1sB_dx_dxhi00_dxxhi(xhi00, xhix, xhix_vec, xs_m, zs_m, I_2lrkl,
                                    J_2lrkl, cctes_2lrkl, a1vdw_2lrkl,
                                    a1vdw_ctekl, dxhix_dxhi00, dxhix_dx,
                                    dxhix_dx_dxhi00)
    a1sb_2r, da1sb_2r, da1sb_2rx, da1sb_2rxxhi = out_2lr
    out_lar = da1sB_dx_dxhi00_dxxhi(xhi00, xhix, xhix_vec, xs_m, zs_m, I_larkl,
                                    J_larkl, cctes_larkl, a1vdw_larkl,
                                    a1vdw_ctekl, dxhix_dxhi00, dxhix_dx,
                                    dxhix_dx_dxhi00)
    a1sb_ar, da1sb_ar, da1sb_arx, da1sb_arxxhi = out_lar

    a1sb_a1 = np.array([[a1sb_a, a1sb_r],
                        [da1sb_a, da1sb_r]])

    a1sb_a2 = np.array([[a1sb_2a, a1sb_ar, a1sb_2r],
                       [da1sb_2a, da1sb_ar, da1sb_2r]])

    a1sb_a1x = np.array([da1sb_ax, da1sb_rx])
    a1sb_a2x = np.array([da1sb_2ax, da1sb_arx, da1sb_2rx])

    a1sb_a1xxhi = np.array([da1sb_axxhi, da1sb_rxxhi])
    a1sb_a2xxhi = np.array([da1sb_2axxhi, da1sb_arxxhi, da1sb_2rxxhi])

    return a1sb_a1, a1sb_a2, a1sb_a1x, a1sb_a2x, a1sb_a1xxhi, a1sb_a2xxhi


def da1sB_dx_d2xhi00_dxxhi_eval(xhi00, xhix, xhix_vec, xs_m, zs_m,
                                I_lambdaskl, J_lambdaskl, ccteskl, a1vdwkl,
                                a1vdw_ctekl, dxhix_dxhi00, dxhix_dx,
                                dxhix_dx_dxhi00):

    # la_kl, lr_kl, la_kl2, lr_kl2, lar_kl = lambdaskl
    cctes_lakl, cctes_lrkl, cctes_2lakl, cctes_2lrkl, cctes_larkl = ccteskl
    a1vdw_lakl, a1vdw_lrkl, a1vdw_2lakl, a1vdw_2lrkl, a1vdw_larkl = a1vdwkl

    I_lakl, I_lrkl, I_2lakl, I_2lrkl, I_larkl = I_lambdaskl
    J_lakl, J_lrkl, J_2lakl, J_2lrkl, J_larkl = J_lambdaskl

    out_la = da1sB_dx_d2xhi00_dxxhi(xhi00, xhix, xhix_vec, xs_m, zs_m, I_lakl,
                                    J_lakl, cctes_lakl, a1vdw_lakl,
                                    a1vdw_ctekl, dxhix_dxhi00, dxhix_dx,
                                    dxhix_dx_dxhi00)
    a1sb_a, da1sb_a, d2a1sb_a, da1sb_ax, da1sb_axxhi = out_la
    out_lr = da1sB_dx_d2xhi00_dxxhi(xhi00, xhix, xhix_vec, xs_m, zs_m, I_lrkl,
                                    J_lrkl, cctes_lrkl, a1vdw_lrkl,
                                    a1vdw_ctekl, dxhix_dxhi00, dxhix_dx,
                                    dxhix_dx_dxhi00)
    a1sb_r, da1sb_r, d2a1sb_r, da1sb_rx, da1sb_rxxhi = out_lr
    out_2la = da1sB_dx_d2xhi00_dxxhi(xhi00, xhix, xhix_vec, xs_m, zs_m,
                                     I_2lakl, J_2lakl, cctes_2lakl,
                                     a1vdw_2lakl, a1vdw_ctekl, dxhix_dxhi00,
                                     dxhix_dx, dxhix_dx_dxhi00)
    a1sb_2a, da1sb_2a, d2a1sb_2a, da1sb_2ax, da1sb_2axxhi = out_2la
    out_2lr = da1sB_dx_d2xhi00_dxxhi(xhi00, xhix, xhix_vec, xs_m, zs_m,
                                     I_2lrkl, J_2lrkl, cctes_2lrkl,
                                     a1vdw_2lrkl, a1vdw_ctekl, dxhix_dxhi00,
                                     dxhix_dx, dxhix_dx_dxhi00)
    a1sb_2r, da1sb_2r, d2a1sb_2r, da1sb_2rx, da1sb_2rxxhi = out_2lr
    out_lar = da1sB_dx_d2xhi00_dxxhi(xhi00, xhix, xhix_vec, xs_m, zs_m,
                                     I_larkl, J_larkl, cctes_larkl,
                                     a1vdw_larkl, a1vdw_ctekl, dxhix_dxhi00,
                                     dxhix_dx, dxhix_dx_dxhi00)
    a1sb_ar, da1sb_ar, d2a1sb_ar, da1sb_arx, da1sb_arxxhi = out_lar

    a1sb_a1 = np.array([[a1sb_a, a1sb_r],
                        [da1sb_a, da1sb_r],
                        [d2a1sb_a, d2a1sb_r]])

    a1sb_a2 = np.array([[a1sb_2a, a1sb_ar, a1sb_2r],
                       [da1sb_2a, da1sb_ar, da1sb_2r],
                       [d2a1sb_2a, d2a1sb_ar, d2a1sb_2r]])

    a1sb_a1x = np.array([da1sb_ax, da1sb_rx])
    a1sb_a2x = np.array([da1sb_2ax, da1sb_arx, da1sb_2rx])

    a1sb_a1xxhi = np.array([da1sb_axxhi, da1sb_rxxhi])
    a1sb_a2xxhi = np.array([da1sb_2axxhi, da1sb_arxxhi, da1sb_2rxxhi])

    return a1sb_a1, a1sb_a2, a1sb_a1x, a1sb_a2x, a1sb_a1xxhi, a1sb_a2xxhi


def x0lambda_evalm(x0, laij, lrij, larij):
    x0la = x0**laij
    x0lr = x0**lrij
    x02la = x0**(2*laij)
    x02lr = x0**(2*lrij)
    x0lar = x0**larij

    # To be used for a1 and a2 in monomer term
    x0_a1 = np.array([x0la, -x0lr])
    x0_a2 = np.array([x02la, -2*x0lar, x02lr])

    return x0_a1, x0_a2


def x0lambda_evalc(x0, la, lr, lar):
    x0la = x0**la
    x0lr = x0**lr
    x02la = x0**(2*la)
    x02lr = x0**(2*lr)
    x0lar = x0**lar

    # To be used for a1 and a2 in monomer term
    x0_a1 = np.array([x0la, -x0lr])
    x0_a2 = np.array([x02la, -2*x0lar, x02lr])
    # To be used in g1 and g2 of chain
    x0_g1 = np.array([la * x0la, -lr*x0lr])
    x0_g2 = np.array([la * x02la, -lar*x0lar, lr * x02lr])

    return x0_a1, x0_a2, x0_g1, x0_g2
