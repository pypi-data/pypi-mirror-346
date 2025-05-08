import torch, os, sys
torch.manual_seed(0) 
from trialbench.dataset import *

from tqdm import tqdm
import requests
import warnings
warnings.filterwarnings("ignore")

def download_all_data(save_path):
    '''
    Download all datasets from zenodo.org
    '''
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    url = "https://zenodo.org/records/14975339/files/all_task.zip?download=1"
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))

    with open(save_path, 'wb') as file, tqdm(
        desc=os.path.basename(save_path),
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                size = file.write(chunk)
                bar.update(size)
    
    print(f"All the datasets are downloaded to: {save_path}")

def load_data(task, phase):
    '''
    Input:
        task: str, name of the dataset
        phase: str, phase of the clinical trial (e.g., "Phase 1", "Phase 2", "Phase 3", "Phase 4")
    Output: [train_loader, valid_loader, test_loader, num_classes, tabular_input_dim
        dataloaders:  tuple, containing train_loader, valid_loader, test_loader
        tabular_input_dim: int, number of features
    '''
    if task == 'mortality_rate':
        return mortality_rate(phase)
    elif task == 'serious_adverse_rate':
        return serious_adverse_rate(phase)
    elif task == 'patient_dropout_rate':
        return patient_dropout_rate(phase)
    elif task == 'duration':
        return duration(phase)
    elif task == 'outcome':
        return outcome(phase)
    elif task == 'failure_reason':
        return failure_reason(phase) 
    elif task == 'serious_adverse_rate_yn':
        return serious_adverse_rate_yn(phase)
    elif task == 'patient_dropout_rate_yn':
        return patient_dropout_rate_yn(phase)
    elif task == 'mortality_rate_yn':
        return mortality_rate_yn(phase)
    elif task == 'dose':
        return dose(phase)
    elif task == 'dose_cls':
        return dose_cls(phase)

def load_model():
    pass

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python function.py <task> <phase>")
        sys.exit(1)

    task = sys.argv[1]
    phase = sys.argv[2]

    train_loader, valid_loader, test_loader, num_classes, tabular_input_dim = load_data(task, phase)
    print(f"train_loader: {len(train_loader)}")
    print(f"num_classes: {num_classes}, tabular_input_dim: {tabular_input_dim}")
