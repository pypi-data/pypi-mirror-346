import ROOT
import argparse
import pandas as pd

"""
Usage: python cutflow_compare.py --file histoOut-compared.root histoOut-referance.root -r region1 region2 region3
"""
def get_file_name(file):
    file_name = file.replace("histoOut-", "")
    file_name = file_name.replace(".root", "")
    return file_name

def main():
    parser = argparse.ArgumentParser(description='Compare cutflow histograms')
    parser.add_argument('-f', '--files', nargs='+', required=True, help='Input ROOT files')
    parser.add_argument('-r', '--regions', nargs='+', required=True, help='Regions to compare')
    args = parser.parse_args()    

    # Parse the input arguments
    files = args.files
    regions = args.regions

    df = pd.DataFrame()
    for file in files:
        f = ROOT.TFile(file)
        file_name = get_file_name(file)
        
        print(f"*** Starting analysis for file: {file} ***")

        for region in regions:
            hc = f.Get(region + "/" + "cutflow")
            nbins = hc.GetXaxis().GetNbins()

            nctot = hc.GetBinContent(0+1)
            labels = []
            contents = []
            for i in range(1, nbins):
                labels.append(hc.GetXaxis().GetBinLabel(i+1))
                contents.append(hc.GetBinContent(i+1))
            df[f"{file_name}_{region}_Selection"] = labels
            df[f"{file_name}_{region}_Event_After_Cut"] = contents
            print(f"*** Finished analysis for file: {file} ***")

    for region in regions:
        
        print(f"*** Starting comparison for region: {region} ***")

        nc = df[f"{get_file_name(files[0])}_{region}_Event_After_Cut"]
        np = df[f"{get_file_name(files[1])}_{region}_Event_After_Cut"] 
        
        df[f"{region}_Error"] = abs((nc - np) / np)

        print(f"*** Finished comparison for region: {region} ***")

    df.to_csv("cutflow_comparison_result.csv", index=False)
                
    print("\n" + "*" * 63)
    print("***Comparison results saved to cutflow_comparison_result.csv***")
    print("*" * 63 + "\n")

if __name__ == "__main__":
    main()