# synaptopHluorin
## Installation and setup (Windows)
Install [Anaconda](https://www.anaconda.com/download) for your operating system. Once installed, open Anaconda which will show the Anaconda.Navigator and then install (if not installed) the Powershell Prompt and click `Launch`.

In the Powershell Prompt, copy and paste the following to install all the packages and dependencies in a new Python environment.

```console
conda create -n synaptophluorin python pandas numpy pathlib scikit-learn scipy tk spyder -c conda-forge
```

Once environment has been created and packages installed (may be slow using Conda), activate the environment by copying and pasting the following into the Powershell Prompt.

```console
conda activate synaptophluorin
```

Download analysis script either by [downloading as a ZIP](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives) or by using the following command (requires [SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh))

```console
git clone git@github.com:AdamDHines/synaptopHluorin-analysis.git
```

Navigate to the folder where the analysis script was downloaded.

```console
cd /<path_to_script>/
```

Launch `Spyder` and open the analysis script to run it.

```console
spyder
```

## Running the analysis
When you run the script, a user dialogue will appear for you to select a folder. Select the parent folder the synaptoPhluorin images were pre-processed in which consists of `Results.csv` files. The analysis script will go through each subfolder and find `Results.csv` to perform the analysis on, so only do one condition at a time.

This script does not output any data, so use the variable explorer in Spyder to get the results.
