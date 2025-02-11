from klein_config import get_config

config = get_config()

####### Dashboard variabel ########

# Interval of Document to Report (statistic)
n_report_i = 0
n_report_f = config.get("dashboard.n_statistic_report")


# Pagination
per_page_number = config.get("dashboard.documents_per_page")