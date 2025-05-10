import ROOT
import argparse
import pandas as pd
from uncertainties import ufloat

"""
Usage: cutflow_compare --files histoOut-compared.root histoOut-reference.root -r region1 region2 region3 --seperate-selections --relative-error
Make sure you use the same names for regions in both .root files.
"""

def get_file_name(file):
    file = file.split("/")[-1]
    file_name = file.replace("histoOut-", "")
    file_name = file_name.replace(".root", "")
    # if from dir was passed,
    return file_name

def main():
    parser = argparse.ArgumentParser(description='Compare cutflow histograms')
    parser.add_argument('-f', '--files', nargs='+', required=True, help='Input ROOT files')
    parser.add_argument('-r', '--regions', nargs='+', required=True, help='Regions to compare')
    parser.add_argument('--separate-selections', action='store_true', help='Keep selections separate instead of merging')
    parser.add_argument('--relative-error', action='store_true', help='Include error in the output')
    args = parser.parse_args()    

    # Parse the input arguments
    files = args.files
    regions = args.regions

    df = pd.DataFrame()
    cont_dict = {}
    for file in files:
        f = ROOT.TFile(file)
        file_name = get_file_name(file)
        if not f.IsOpen():
            print(f"Error: File {file} could not be opened.")
            raise SystemExit(1)

        print(f"*** Starting analysis for file: {file} ***")
        
        for region in regions:

            if not f.Get(region + "/" + "cutflow"):
                print(f"Error: No cutflow histogram found in file {file}.")
                raise SystemExit(1)
            
            hc = f.Get(region + "/" + "cutflow")
            nbins = hc.GetXaxis().GetNbins()

            nctot = hc.GetBinContent(0+1)
            labels = []
            contents = []
            contents_errored = []
            for i in range(1, nbins):
                labels.append(hc.GetXaxis().GetBinLabel(i+1))
                contents.append(ufloat(hc.GetBinContent(i+1), hc.GetBinError(i+1)))
                contents_errored.append(f"{hc.GetBinContent(i+1)} ±{hc.GetBinError(i+1)}")
            

            if args.separate_selections:
                df[f"{file_name}_{region}_Selection"] = labels
            else: 
                df["Selection"] = labels
            df[f"{file_name}_{region}_Event_After_Cut"] = contents_errored
            cont_dict[f"{file_name}_{region}_Event_After_Cut_ufloat"] = contents
            print(f"*** Finished analysis for file: {file} ***")

    if args.relative_error:
        print(cont_dict)
        error_df = pd.DataFrame.from_dict(cont_dict)
        print(error_df)
        for region in regions:
            
            print(f"*** error calculation: {region} ***")

            nc = error_df[f"{get_file_name(files[0])}_{region}_Event_After_Cut_ufloat"]
            np = error_df[f"{get_file_name(files[1])}_{region}_Event_After_Cut_ufloat"] 
            
            df[f"{region}_Error"] = (abs((nc - np) / np))

            print(f"*** Finished error calculation: {region} ***")

    df.to_csv("cutflow_comparison_result.csv", index=False)
                
    print("\n" + "*" * 63)
    print("***Comparison results saved to cutflow_comparison_result.csv***")
    print("*" * 63 + "\n")

if __name__ == "__main__":
    main()