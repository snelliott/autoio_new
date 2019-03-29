""" electronic energy readers
"""
import autoparser as apr
from autoparse import cast as _cast
import autoparse.pattern as app
import autoparse.find as apf
import elstruct.par


def _hf_energy(output_string):
    ene = apr.energy.read(
        output_string,
        app.one_of_these([
            app.escape('E(RHF) ='),
            app.escape('E(UHF) ='),
            app.escape('E(ROHF) =')]))
    return ene


def _mp2_energy(output_string):
    ene_d_str = apr.energy.read(
        output_string,
        app.escape('EUMP2 = '),
        val_ptt=app.EXPONENTIAL_FLOAT_D)
    ene = _cast(apf.replace('d', 'e', ene_d_str, case=False))
    return ene


def _dft_energy_(func_name):

    def _dft_energy(output_string):
        ene = apr.energy.read(
            output_string,
            app.one_of_these([
                app.escape('E(R{}) ='.format(func_name)),
                app.escape('E(U{}) ='.format(func_name))]),
            case=False)  # this is the default, but as a reminder
        return ene

    return _dft_energy


# a dictionary of functions for reading the energy from the output, by method
ENERGY_READER_DCT = {
    elstruct.par.Method.HF: _hf_energy,
    elstruct.par.Method.Corr.MP2: _mp2_energy,
    elstruct.par.Method.Dft.B3LYP: _dft_energy_('b3lyp'),
    elstruct.par.Method.Dft.WB97XD: _dft_energy_('wb97xd'),
}


def method_list():
    """ list of available electronic structure methods
    """
    return tuple(sorted(ENERGY_READER_DCT.keys()))


def energy(method, output_string):
    """ get total energy from output
    """
    method = method.lower()
    assert method in method_list()
    # get the appropriate reader and call it
    energy_reader = ENERGY_READER_DCT[method]
    return energy_reader(output_string)
