"""
Copyright (c) 2019-2020 RoZetta Technology Pty Ltd. All rights reserved.

This may need to be replaced by other service ?
"""

COMPONENT_MAPPING = {
    'ftplistbuilder': 'datahex.audit.downloader.ftplistbuilder',
    'ftp_downloader': 'datahex.audit.downloader.ftp_downloader',
    'zip2gz': 'datahex.audit.ecsprocs.zip2gz',
    'ms_transform': 'datahex.audit.dbsproc.ms_transform',
    'map_etl_dag': 'datahex.audit.workflow.map_etl_dag',
    'data_induction_dag': 'datahex.audit.workflow.data_induction_dag',
    'simple_pipeline_copy_dag': 'datahex.audit.workflow.simple_pipeline_copy_dag',
    'upload_csv_to_parquet_dag': 'datahex.audit.workflow.upload_csv_to_parquet_dag',
    'parquet2table': 'datahex.audit.dbsproc.parquet2table',
    'csv2parquets': 'datahex.audit.dbsproc.csv2parquets',
    'dpu': 'datahex.audit.dpu',
    'catalog': 'datahex.audit.catalog',
    'oms': 'datahex.audit.oms',
    'pipeline-mgmt': 'datahex.audit.pipeline-mgmt'
}


def get_source(component):
    """
    Returns the source information from component
    """
    return COMPONENT_MAPPING.get(component, 'undefined_source')
