# Differentially expressed genes plot

### Walkthrough

First, make sure you have installed an environment with suitable packages for this visualization.
To install a virtual environment using Python3 and activate it:
`python3 -m venv <env_name>`
`source <env_name>/bin/activate`
To install related packages:
`pip install pandas plotly dash dash_bio`


Next, create simple Dash app with VolcanoPlot, the tutorial can be found here.
Designate a port on your localhost:
`app.run_server(debug=True, port=8050)`

To run the app, make sure you know where's the data (and the format):
`python3 app.py --data_path <path_name>`


### References
