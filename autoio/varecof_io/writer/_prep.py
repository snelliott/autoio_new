""" Generate the information necessary to product the vrctst input files
"""

import automol


def intramolecular_constraint_dct(inf_sep_zma, rct_zmas):
    """ Set the additional constraints for the constrained MEP,
        constrains all of the intramolecular constraint_dct

        maybe just separate inf sep zma anf get the frag atoms
        sort of assumes the zma is frag1_zma + frag2_zma
    """

    frag1_natom = automol.zmat.count(rct_zmas[0])
    frag2_natom = automol.zmat.count(rct_zmas[1])

    # Build pairs for intermolecular coords to optimize:
    #   (zma_atom_idx, coord_idx in row) (uses 0-indexing)
    # frag1_natom, 0 is the scan coord already accounted for
    no_frz_idxs = []
    no_frz_idxs.append([frag1_natom, 0])
    no_frz_idxs.append([frag1_natom, 1])
    no_frz_idxs.append([frag1_natom, 2])
    if frag2_natom == 2:
        no_frz_idxs.append([frag1_natom+1, 1])
        no_frz_idxs.append([frag1_natom+1, 2])
    elif frag2_natom > 2:
        no_frz_idxs.append([frag1_natom+1, 1])
        no_frz_idxs.append([frag1_natom+1, 2])
        no_frz_idxs.append([frag1_natom+2, 1])

    # Now grab the coordinates NOT in the opt coord idxs
    alt_froz_coords = []
    name_matrix = automol.zmat.name_matrix(inf_sep_zma)
    for row_idx, row in enumerate(name_matrix):
        for coord_idx, coord in enumerate(row):
            if [row_idx, coord_idx] not in no_frz_idxs:
                if coord is not None:
                    alt_froz_coords.append(coord)

    # Now build the constraint dictionary
    zma_vals = automol.zmat.value_dictionary(inf_sep_zma)
    constraint_dct = dict(zip(
        alt_froz_coords, (zma_vals[name] for name in alt_froz_coords)))

    return constraint_dct


def fragment_geometries(ts_zma, rct_zmas, bnd_keys):
    """ Generate the fragment geometries from the ts Z-matrix and the
        indices involved in the forming bond
    """

    min_idx, max_idx = min(bnd_keys), max(bnd_keys)

    # Get geometries of fragments from the ts_zma from the MEP
    mep_total_geo = automol.zmat.geometry(ts_zma)
    mep_fgeos = [mep_total_geo[:max_idx], mep_total_geo[max_idx:]]

    # Get geometries of isolated fragments at infinite sepearation
    iso_fgeos = [automol.zmat.geometry(zma) for zma in rct_zmas]

    # Reorder the iso_fgeos to line up with the mep_frag_geos
    (iso1_symbs, iso2_symbs) = (automol.geom.symbols(geo) for geo in iso_fgeos)
    (mep1_symbs, mep2_symbs) = (automol.geom.symbols(geo) for geo in mep_fgeos)
    if iso1_symbs != mep1_symbs or iso2_symbs != mep2_symbs:
        iso_fgeos[0], iso_fgeos[1] = iso_fgeos[1], iso_fgeos[0]

    # Get the geometries for the structure.inp file
    iso_fgeos_wdummy = []
    mol_data = zip(mep_fgeos, iso_fgeos, (max_idx, min_idx))
    for i, (mep_fgeo, iso_fgeo, idx) in enumerate(mol_data):

        if not automol.geom.is_atom(mep_fgeo):

            # Build MEPFragGeom+X coordinates using MEP geometry
            # x_idx: index for geom to place dummy X atom
            # a1_idx: index corresponding to "bonding" atom in geometry
            x_coord = mep_total_geo[idx][1]
            dummy_row = ('X', x_coord)
            if i == 0:
                mep_geo_wdummy = mep_fgeo + (dummy_row,)
                x_idx = len(mep_geo_wdummy) - 1
                a1_idx = 0
            else:
                mep_geo_wdummy = (dummy_row,) + mep_fgeo
                x_idx = 0
                a1_idx = 1

            # Set a2_idx to a1_idx + 1; should not be any restrictions
            a2_idx = a1_idx + 1

            # Set a3_idx.
            # Need to ensure idx does NOT correspond to atom where x = 0.0
            # The internal xyzp routine dies in this case
            for idx2 in range(a2_idx+1, len(iso_fgeo)):
                if not iso_fgeo[idx2][1][0] == 0.0:
                    a3_idx = idx2
                    break

            # Calculate coords to define X position in IsoFragGeom structure
            xyz1 = iso_fgeo[a1_idx][1]
            xyz2 = iso_fgeo[a2_idx][1]
            xdistance = automol.geom.distance(
                mep_geo_wdummy, x_idx, a1_idx)
            xangle = automol.geom.central_angle(
                mep_geo_wdummy, x_idx, a1_idx, a2_idx)
            if len(mep_fgeo) > 2:
                xyz3 = iso_fgeo[a3_idx][1]
                xdihedral = automol.geom.dihedral_angle(
                    mep_geo_wdummy, x_idx, a1_idx, a2_idx, a3_idx)
            else:
                xyz3 = 0.0
                xdihedral = 0.0

            # Calculate the X Position for the IsoFrag structure
            xyzp = automol.util.vec.from_internals(
                dist=xdistance, xyz1=xyz1, ang=xangle, xyz2=xyz2,
                dih=xdihedral, xyz3=xyz3)
            # xyzp = automol.geom.find_xyzp_using_internals(
            #     xyz1, xyz2, xyz3, xdistance, xangle, xdihedral)

            # Generate the IsoFragGeom+X coordinates for the structure.inp file
            if i == 0:
                iso_geo_wdummy = iso_fgeo + (('X', xyzp),)
            else:
                iso_geo_wdummy = (('X', xyzp),) + iso_fgeo

            # Append to final geoms
            iso_fgeos_wdummy.append(iso_geo_wdummy)

        else:
            # If atom, set IsoFragGeom+X coords equal to mep_geo
            iso_fgeos_wdummy.append(mep_fgeo)

    # return mep_total_geo, iso_fgeos, iso_fgeos_wdummy
    return mep_total_geo, iso_fgeos_wdummy


# def assess_face_symmetries(divsur_out_string):
def assess_face_symmetries(fgeo1, fgeo2):
    """ check the symmetry of the faces for each fragment

        :param fgeo1: fragment geometry 1
        :type fgeo1: molecular geometry 1
    """

    # Read fragment geoms from divsur.out with coordinates in the divsur frame
    # fgeo1, fgeo2 = varecof_io.reader.divsur.frag_geoms_divsur_frame(
    #     divsur_out_string)
    # fgeos = [automol.geom.from_string(fgeo1),
    #          automol.geom.from_string(fgeo2)]

    # Check facial symmetry if fragments are molecules
    symms = [False, False]
    # for i, fgeo in enumerate(fgeos):
    for i, fgeo in enumerate((fgeo1, fgeo2)):
        if not automol.geom.is_atom(fgeo):
            # Reflect the dummy atom (pivot position) about the xy plane
            if i == 0:
                dummy_idx = len(fgeo) - 1
            else:
                dummy_idx = 0
            fgeo_reflect = automol.geom.reflect_coordinates(
                fgeo, [dummy_idx], ['x', 'y'])
            # Compute Coloumb spectrum for each geom to its reflected version
            symms[i] = automol.geom.almost_equal_coulomb_spectrum(
                fgeo, fgeo_reflect, rtol=5e-2)

    # Set the face and face_sym keywords based on the above tests
    [symm1, symm2] = symms
    if symm1 and symm2:
        faces = [0, 1]
        face_symm = 4
    elif symm1 and not symm2:
        faces = [0, 1]
        face_symm = 2
    elif not symm1 and symm2:
        faces = [0, 1]
        face_symm = 2
    elif not symm1 and not symm2:
        faces = [0]
        face_symm = 1

    return faces, face_symm


# FUNCTIONS TO SET UP THE DIVIDING SURFACE FRAMES
def build_pivot_frames(total_geom, frag_geos_wdummy, bnd_keys):
    """ Use geometries to get pivot info only set up for 1 or 2 pivot points
    """

    bnd_keys = sorted(list(bnd_keys))
    print('bndk', bnd_keys)

    frames, npivots, = [], []
    for i, (rxn_idx, geo) in enumerate(zip(bnd_keys, frag_geos_wdummy)):

        geom = automol.geom.without_dummy_atoms(geo)

        # Single pivot point centered on atom
        if automol.geom.is_atom(geom):
            # Single pivot point centered on atom
            npivot = 1
            frame = [0, 0, 0, 0]
        elif automol.geom.is_linear(geom):
            # For linear species we place the pivot point on radical
            # with no displacment, so no need to find coordinates
            npivot = 2
            frame = [0, 0, 0, 0]
        else:
            # else we build an xy frame to easily place pivot point
            npivot = 2

            print('gota geom\n', total_geom)
            # Find the idx in each fragment bonded to the atom at the pivot pt
            for j, coords in enumerate(geom):
                print(coords)
                if coords == total_geom[rxn_idx]:
                    coord_idx = j
                    break

            # For each fragment, get indices for a
            # chain (up to three atoms, that terminates at the dummy atom)
            gra = automol.geom.graph(geom)
            gra_neighbor_dct = automol.graph.atoms_neighbor_atom_keys(gra)
            bond_neighbors = gra_neighbor_dct[coord_idx]

            # Find idx in each fragment geom that corresponds to the bond index
            for j, idx in enumerate(bond_neighbors):
                if geom[idx][0] != 'H':
                    bond_neighbor_idx = idx
                    break
                if geom[idx][0] == 'H' and j == (len(bond_neighbors) - 1):
                    bond_neighbor_idx = idx

            # Set up the frame indices for the divsur file
            if i == 0:
                pivot_idx = len(geom)
                frame = [coord_idx, bond_neighbor_idx, pivot_idx, coord_idx]
            else:
                pivot_idx = 0
                coord_idx += 1
                bond_neighbor_idx += 1
                frame = [coord_idx, bond_neighbor_idx, pivot_idx, coord_idx]
            frame = [val+1 for val in frame]

        # Append to lists
        frames.append(frame)
        npivots.append(npivot)

    return frames, npivots


def calc_pivot_angles(frag_geos_wdummy, frames):
    """ get the angle for the three atoms definining the frame
    """

    angles = tuple()
    for geo_wdummy, frame in zip(frag_geos_wdummy, frames):
        geo_ndum = automol.geom.without_dummy_atoms(geo_wdummy)
        if automol.geom.is_atom(geo_ndum) or automol.geom.is_linear(geo_ndum):
            angle = None
        else:
            frame = [val-1 for val in frame]
            angle = automol.geom.central_angle(
                geo_wdummy, frame[2], frame[0], frame[1])

        angles += (angle,)

    return angles


def calc_pivot_xyzs(total_geom, frag_geos, bnd_keys):
    """ figure out where pivot point will be centered
        only linear speces need to have non-zero xyz, as they
        will not have a frame set up for them like atoms and
        polyatomics
    """

    bnd_keys = sorted(list(bnd_keys))

    xyzs = tuple()
    for rxn_idx, geo in zip(bnd_keys, frag_geos):
        if automol.geom.is_linear(geo):
            xyz = total_geom[rxn_idx][1]
        else:
            xyz = (0.0, 0.0, 0.0)

        xyzs += (xyz,)

    return xyzs
