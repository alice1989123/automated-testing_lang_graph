import logging
import logger

from pyspark.sql.functions import col, lit
from utils import init_spark


logger_instance = logger.Logger()

class CleanLogs:
    
    def __init__(self) -> None:
        
        self.spark = init_spark.run()
       
    def clean_path(self,data,path,partition_day,layer_attributes_path):
        
        select_colums = list({key for dictionary in layer_attributes_path for key in dictionary.keys()})
        data = data.select(*select_colums)
        data = self.homologate_attributes(data,layer_attributes_path,partition_day,path)
        return data
        
              
    def default_value(self,column, tipo):
        
        columns_string_diff_value = {
            "inf_perfi_dis_user": "false",
            "inf_perfi_dis_ip": "0.0.0.0"
            }
            
        # caso para información financiera y personal deel cliente
        if column in columns_string_diff_value:
            return lit(columns_string_diff_value[column])
        
        elif tipo == "boolean":
            return lit("false")
        elif (tipo == "integer") and (column == "inf_sucursal"):
            return lit(9999)
        elif tipo == "integer":
            return lit(0)
        elif tipo == "date":
            return lit("2023-01-01 00:00:00")
        elif tipo == "string":
            return lit("unspecified")
        
            
    def homologate_attributes(self,data,type_columns,partition_day,path):
        
        for attribute in type_columns :
            column, type_column = next(iter(attribute.items()))
            data = data.withColumn(column, col(column).cast(type_column))
        
        data = data.withColumn("path",lit(path))\
            .withColumn("execution_day", lit(partition_day))
            
        return data
            