$Env:CONDA_EXE = "/Users/jakobbull/Documents/Yenching/Financial Econometrics/project/ENTER/bin/conda"
$Env:_CE_M = ""
$Env:_CE_CONDA = ""
$Env:_CONDA_ROOT = "/Users/jakobbull/Documents/Yenching/Financial Econometrics/project/ENTER"
$Env:_CONDA_EXE = "/Users/jakobbull/Documents/Yenching/Financial Econometrics/project/ENTER/bin/conda"
$CondaModuleArgs = @{ChangePs1 = $True}
Import-Module "$Env:_CONDA_ROOT\shell\condabin\Conda.psm1" -ArgumentList $CondaModuleArgs

Remove-Variable CondaModuleArgs