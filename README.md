# Medical Informatics

## Requirements

- Python (Anaconda or Miniconda)

- IDE (Spyder / Jupyter Lab / Vs Code, ...)

- Conda env:

  - ```
    conda create -n mi python=3.13
    conda activate mi
    pip install -r requirements
    ```

- Add env kernel to jupyter (inside the created conda env):

  - ```
    python -m ipykernel install --user --name mi --display-name "MI Env"
    ```

    > [!NOTE]
    >
    > You can get the list of jupyter kernels:
    >
    > ```
    > jupyter kernelspec list
    > ```
    >
    > You can remove the env from jupyter with the following command:
    >
    > ```
    > jupyter kernelspec remove mi
    > ```

---

## Run Codes

- For **notebooks**, run `jupyter lab` and select the `mi` kernel

- For `.py` **codes**, first activate the env, then run from cmd:

  - ```
    conda activate mi
    python filename.py
    ```

    > [!NOTE]
    >
    > You can use the created env in **Spyder** by changing the interpreter:
    >
    > - Tools --> Preferences --> Python Interpreter --> Select interpreter 
    >
    > - Restart the kernel or Spyder
    >
    > It will require you to install spyder-kernel:
    >
    > ```
    > pip install spyder-kernels==3.1.*
    > ```