i get below msg, i guess its now allowing me to do anything due to access, but earlier i did for numpy and statesmodel right, guide me correctly to solve this pandas issue 


(base) C:\Windows\System32>conda install pandas=2.2.2 statsmodels=0.14.2 --force-reinstall
Channels:
 - defaults
Platform: win-64
Collecting package metadata (repodata.json): done
Solving environment: done

## Package Plan ##

  environment location: C:\Program Files\Anaconda3_2024_10_1

  added / updated specs:
    - pandas=2.2.2
    - statsmodels=0.14.2


The following NEW packages will be INSTALLED:

  ucrt               pkgs/main/win-64::ucrt-10.0.22621.0-haa95532_0
  vc14_runtime       pkgs/main/win-64::vc14_runtime-14.44.35208-h4927774_12

The following packages will be UPDATED:

  ca-certificates                      2024.9.24-haa95532_0 --> 2026.5.14-haa95532_0
  certifi                         2024.8.30-py312haa95532_0 --> 2026.6.17-py312haa95532_0
  conda                              24.9.2-py312haa95532_0 --> 24.11.3-py312haa95532_0
  openssl                                 3.0.15-h827c3e9_0 --> 3.5.7-hbb43b14_0
  vs2015_runtime                     14.40.33807-h98bb1dd_1 --> 14.44.35208-ha6b5a95_12


Proceed ([y]/n)? [y]
Invalid choice: [y]
Proceed ([y]/n)? y


Downloading and Extracting Packages:

Preparing transaction: done
Verifying transaction: failed

EnvironmentNotWritableError: The current user does not have write permissions to the target environment.
  environment location: C:\Program Files\Anaconda3_2024_10_1



(base) C:\Windows\System32>
