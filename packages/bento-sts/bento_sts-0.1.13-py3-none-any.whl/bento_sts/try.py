from bento_sts.query import Query
import yaml

qp = yaml.load(open("config_sts/query_paths.yml","r"), Loader=yaml.CLoader)
Query.set_paths(qp)
qq = Query("terms/model-pvs/goob/1.0.0/pvs")
qq = Query("terms/cde-pvs/112443/1.00/pvs")
qq = Query("term/by-origin/caDSR/12035768")
qq = Query("term/by-origin/caDSR/12035768/1.00")
pass
