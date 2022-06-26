app:
	streamlit run dashboard/dashboard.py

env:
	python3 -m venv .venv

install:
	python -m pip install --index-url http://nexus.prod.uci.cu/repository/pypi-proxy/simple/ --trusted-host nexus.prod.uci.cu

update-reqs:
	python3 -m pip freeze > requirements.txt
