# pyTSPA - Toolbox for Analyzing and Visualizing Team Sports Performance  

A toolbox for analyzing and visualizing team sports performance, with a particular focus on **football match data**.  
The toolbox includes modules for data processing, statistical analysis, match outcome prediction, and result visualization.

---

### Current Version: `0.1.1`  
### Planned Release: May 2025  

---

## Introduction  

`pyTSPA` was developed to support coaches, analysts, and sports scientists in extracting actionable insights from football match data.  
Designed with a **football-centric approach**, the toolbox facilitates data handling, statistical analysis, match outcome prediction using machine learning, and comprehensive data visualization.

---

## Description  

The toolbox is divided into the following modules:

- **Data Handling:**  
  - Data input/output, cleaning, and profiling (CSV, Excel).

- **Metrics:**  
  - Calculation of match and team statistics (`Win Percentage`, `Pythagorean Expectation`)  
  - Predictive models using **logistic regression** for match outcome prediction.

- **Visualization:**  
  - Graphical representation of match data, statistical summaries, and prediction results using bar charts, scatter plots, and pie charts.

---

**For more information, visit the [official documentation](https://pytspa-toolbox.readthedocs.io/en/latest/)**.


## Installation
### From PyPi
Install `pyTSPA` using pip

```
pip install pyTSPA-toolbox
```

### From source
Clone the git repository
```
git clone https://github.com/vargaheni05/pyTSPA-toolbox.git
```
Change directory to the cloned repository
```
cd pyTSPA-toolbox
```
Install with pip
```
pip install .
```

## Building the documentation
Install required packages
```
pip install -r docs/requirements.txt
```
Call Sphinx build command
```
sphinx-build -M html docs/source docs/build
```
On Windows you can also run the `make.bat` file
```
.\docs\make.bat html
```

The documentation should be available in the `docs/build` directory as html files<br>
This includes the example codes as tutorials

## Correspondence
Henrietta Varga (varga.henrietta.julianna@hallgato.ppke.hu)<br>
Marcell Szögi (szogi.marcell@hallgato.ppke.hu)<br>
Benedek Kardos (kardos.benedek.zoltan@hallgato.ppke.hu)
