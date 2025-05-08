def ass_convmat_asmatquad(W=None, invindsw=None):
    """ assemble the convection matrix H, so that N(v)v = H[v.v]

    for the inner nodes.

    Notes
    -----
    Implemented only for 2D problems

    """
    mesh = W.mesh()
    deg = W.ufl_element().degree()
    fam = W.ufl_element().family()

    V = dolfin.FunctionSpace(mesh, fam, deg)

    # this is very specific for V being a 2D VectorFunctionSpace
    invindsv = invindsw[::2]/2

    v = dolfin.TrialFunction(V)
    vt = dolfin.TestFunction(V)

    def _pad_csrmats_wzerorows(smat, wheretoput='before'):
        """add zero rows before/after each row

        """
        indpeter = smat.indptr
        auxindp = np.c_[indpeter, indpeter].flatten()
        if wheretoput == 'after':
            smat.indptr = auxindp[1:]
        else:
            smat.indptr = auxindp[:-1]

        smat._shape = (2*smat.shape[0], smat.shape[1])

        return smat

    def _shuff_mrg_csrmats(xm, ym):
        """shuffle merge csr mats [xxx],[yyy] -> [xyxyxy]

        """
        xm.indices = 2*xm.indices
        ym.indices = 2*ym.indices + 1
        xm._shape = (xm.shape[0], 2*xm.shape[1])
        ym._shape = (ym.shape[0], 2*ym.shape[1])
        return xm + ym

    nklist = []
    for i in invindsv:
        # for i in range(V.dim()):
        # iterate for the columns

        # get the i-th basis function
        bi = dolfin.Function(V)
        bvec = np.zeros((V.dim(), ))
        bvec[np.int(i)] = 1
        bi.vector()[:] = bvec

        # assemble for the i-th basis function
        nxi = dolfin.assemble(v * bi.dx(0) * vt * dx)
        nyi = dolfin.assemble(v * bi.dx(1) * vt * dx)

        nxim = mat_dolfin2sparse(nxi)
        nxim.eliminate_zeros()

        nyim = mat_dolfin2sparse(nyi)
        nyim.eliminate_zeros()

        # resorting of the arrays and inserting zero columns
        nxyim = _shuff_mrg_csrmats(nxim, nyim)
        nxyim = nxyim[invindsv, :][:, invindsw]
        nyxxim = _pad_csrmats_wzerorows(nxyim.copy(), wheretoput='after')
        nyxyim = _pad_csrmats_wzerorows(nxyim.copy(), wheretoput='before')

        # tile the arrays in horizontal direction
        nklist.extend([nyxxim, nyxyim])

    hmat = sps.hstack(nklist, format='csc')
    return hmat

