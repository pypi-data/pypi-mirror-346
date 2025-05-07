<img src="images/Logos.png" alt="Project Logos" width="70%"/>

# **Copernicus Seasonal Forecast Module** 

<img src="images/repo_qr.png" alt="Repository QR Code" width="150"/>

This repository hosts the **copernicus_climada_seasonal_forecast** package, a Python module developed as part of the [U-CLIMADAPT project](https://www.copernicus-user-uptake.eu/user-uptake/details/responding-to-the-impact-of-climate-change-u-climadapt-488).

The module connects **seasonal forecast data** from the [Copernicus Climate Data Store (CDS)](https://cds.climate.copernicus.eu) with flexible data processing and climate impact modeling tools. It includes robust functionality to [**download hourly seasonal forecast data**](https://cds.climate.copernicus.eu/datasets/seasonal-original-single-levels?tab=overview) and automatically **convert it to daily resolution**, enabling a wide range of climate analyses beyond just heat-related indices.

Users can leverage the package to:
- Convert raw Copernicus seasonal forecasts into usable daily datasets.
- Compute **custom or predefined climate indices** (e.g., Heatwaves, Tropical Nights).
- Generate **CLIMADA-compatible hazard objects** from processed data to support **impact-based forecasting** and risk assessment workflows.

While the package is not part of the core [CLIMADA](https://climada.ethz.ch/) platform, it is designed for **tight integration** with it, supporting **end-to-end workflows** from raw data acquisition to risk estimation and adaptation planning.

## **Documentation**

## **Installation**

You can install **copernicus-seasonal-forecast-tools** in three ways:

### 1. Install via pip (recommended for most users)

```bash
pip install copernicus-seasonal-forecast-tools
```
### 2. Install via conda or mamba
```bash
conda install -c conda-forge copernicus-seasonal-forecast-tools
```
### 3. Install directly from GitHub 
```bash
git clone https://github.com/your-username/copernicus-seasonal-forecast-tools.git
cd climada_copernicus_seasonal_forecast
pip install .
```
### **CLIMADA Installation**
If you want to create a hazard object, you need to install **CLIMADA** as a dependency.  

Follow the steps below:
```bash
# 1. Clone the CLIMADA repository

git clone https://github.com/CLIMADA-project/climada_python.git

# 2. Install CLIMADA in development mode
cd climada_python
pip install -e .
cd ..

# 3. Update your environment with the rest of the dependencies if needed
pip install -e .

# 4. Verify the installation
python -c "from climada.hazard import Hazard; print('Hazard module successfully imported!')"
```


## **Example of use**

This repository provides Jupyter Notebooks to work with **CLIMADA** and the **Copernicus seasonal forecast module**.

There are two notebooks available:

- **`Modul_climada_copernicus_seasonal_forecast_workshop.ipynb`**: This is the first notebook to run. It demonstrates how to install and use the `copernicus_interface` module to download, process, and convert seasonal forecast data into a CLIMADA hazard object.
- **`DEMO_Modul_climada_copernicus_seasonal_forecast_workshop.ipynb`**: This is the second notebook. It provides a full example application of the seasonal forecast hazard data in an end-to-end climate impact assessment pipeline.

### Notebooks

| Notebook | Open in Colab | GitHub Link |
|----------|----------------|-------------|
| `Modul_climada_copernicus_seasonal_forecast_workshop.ipynb` | [<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" height="20">](https://colab.research.google.com/github/DahyannAraya/climada_copernicus_seasonal_forecast_workshop/blob/main/Modul_climada_copernicus_seasonal_forecast_workshop.ipynb) | [View on GitHub](https://github.com/DahyannAraya/climada_copernicus_seasonal_forecast_workshop/blob/main/Modul_climada_copernicus_seasonal_forecast_workshop.ipynb) |
| `DEMO_Modul_climada_copernicus_seasonal_forecast_workshop.ipynb` | [<img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" height="20">](https://colab.research.google.com/github/DahyannAraya/climada_copernicus_seasonal_forecast_workshop/blob/main/DEMO_Modul_climada_copernicus_seasonal_forecast_workshop.ipynb) | [View on GitHub](https://github.com/DahyannAraya/climada_copernicus_seasonal_forecast_workshop/blob/main/DEMO_Modul_climada_copernicus_seasonal_forecast_workshop.ipynb) |

---

### Run in Colab

1. Click on **Open in Colab** for the notebook of interest.
2. Make sure you follow all the setup cells in the notebook to install **CLIMADA** and its dependencies.

---

### Run Locally

If you plan to run this notebook locally, you must first install **CLIMADA** and all required dependencies on your system.  
👉 For detailed instructions, follow the official CLIMADA installation guide:  
**[CLIMADA Installation Guide](https://climada-python.readthedocs.io/en/stable/guide/install.html)**

After installing CLIMADA, you should also install the **seasonal forecast module** by following the instructions in the document below:  
👉 [Copernicus Forecast Module Installation Instructions (PDF)](https://drive.google.com/file/d/1NpAslBYLbhUb3W55D43qIWu0zJPCPoAJ/view?usp=sharing)

Alternatively, you can install the module manually by cloning the repository:

```bash
git clone https://github.com/DahyannAraya/climada_copernicus_seasonal_forecast_workshop.git
cd climada_copernicus_seasonal_forecast_workshop
```

## **References**
- [Copernicus Seasonal Forecast Module](https://github.com/CLIMADA-project/climada_petals/tree/feature/copernicus_forecast)
- [Seasonal forecast daily and subdaily data on single levels](https://cds.climate.copernicus.eu/datasets/seasonal-original-single-levels?tab=overview)
- [Copernicus Climate Data Store](https://cds.climate.copernicus.eu)
- [CLIMADA Documentation](https://climada.ethz.ch/)
- [U-CLIMADAPT Project](https://www.copernicus-user-uptake.eu/user-uptake/details/responding-to-the-impact-of-climate-change-u-climadapt-488)
