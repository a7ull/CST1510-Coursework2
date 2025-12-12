from multi_domain_platform.models.dataset import get_all_datasets, Dataset

def get_all_datasets_page():
    return get_all_datasets()

def add_dataset_page(dataset_id, name, rows, columns, uploaded_by, upload_date):
    ds = Dataset(dataset_id, name, rows, columns, uploaded_by, upload_date)
    ds.save()

def delete_dataset_page(dataset_id):
    ds = Dataset(dataset_id, None, None, None, None, None)
    ds.dataset_id = dataset_id
    ds.delete()