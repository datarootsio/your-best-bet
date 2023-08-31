

def model(dbt, session):
    dbt.config(
        submission_method="all_purpose_cluster",
        create_notebook=True,
        cluster_id="0831-063805-6ugeg356"
    )
    
    sparkDF = dbt.ref("match")
    
    # df = sparkDF.toPandas()
    
    return sparkDF.limit(100)
