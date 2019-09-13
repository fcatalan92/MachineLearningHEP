#############################################################################
##  © Copyright CERN 2018. All rights not expressly granted are reserved.  ##
##                 Author: Gian.Michele.Innocenti@cern.ch                  ##
## This program is free software: you can redistribute it and/or modify it ##
##  under the terms of the GNU General Public License as published by the  ##
## Free Software Foundation, either version 3 of the License, or (at your  ##
## option) any later version. This program is distributed in the hope that ##
##  it will be useful, but WITHOUT ANY WARRANTY; without even the implied  ##
##     warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    ##
##           See the GNU General Public License for more details.          ##
##    You should have received a copy of the GNU General Public License    ##
##   along with this program. if not, see <https://www.gnu.org/licenses/>. ##
#############################################################################

import os
import pickle
import argparse
import yaml
from ROOT import TFile, TH1F # pylint: disable=import-error, no-name-in-module
from machine_learning_hep.utilities import openfile
from machine_learning_hep.selectionutils import getnormforselevt

def main():
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('--case', metavar='text', default='DsPbPb010')
    case = parser.parse_args().case
    with open(f"data/database_ml_parameters_{case}.yml", 'r') as param_config:
        data_param = yaml.load(param_config, yaml.FullLoader)

    namefile_evt = data_param[case]["files_names"]["namefile_evt"]
    folder = data_param[case]["multi"]["data"]["pkl_evtcounter_all"]
    path = os.path.join(folder, namefile_evt)

    df_evt_all = pickle.load(openfile(path, 'rb'))
    nselevt = len(df_evt_all.query("is_ev_rej==0"))
    norm = getnormforselevt(df_evt_all)
    print(f'Normalisation: {norm:.3e}')
    print(f'Selected events: {nselevt:.3e}')

    hNorm = TH1F("hEvForNorm", ";;Normalisation", 2, 0.5, 2.5)
    hNorm.GetXaxis().SetBinLabel(1, "normsalisation factor")
    hNorm.GetXaxis().SetBinLabel(2, "selected events")
    hNorm.SetBinContent(1, norm)
    hNorm.SetBinContent(2, nselevt)

    outfile = TFile("Normalisation_%s.root" % case, "recreate")
    hNorm.Write()
    outfile.Close()

main()
