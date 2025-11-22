import pandas as pd
import uvicorn
from src.backend.plots import Plots
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

app = FastAPI(title="Data Visualization Tool")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def main():
    return{
        "message": "STATUS OK"
    }

@app.post("/get_summary")
async def get_summary(filename: str):
    csv_file = pd.read_csv(filename)
    summary_dict = {
        "Shape": csv_file.shape,
        "Headers": csv_file.columns.tolist(),
        "Columns": csv_file.columns.tolist(),
        "Num Cols": csv_file.select_dtypes(include=['int', 'int64', 'int32']).columns.tolist(),
        "Cat Cols": csv_file.select_dtypes(include=['object']).columns.tolist(),
        "Data Types": {c: str(d) for c, d in csv_file.dtypes.items()},
        "Summary": csv_file.describe().to_dict(),
        "Missing Values": csv_file.isnull().sum().to_dict(),
        "Unique Values": csv_file.nunique().to_dict()
    }
    # print("SUMMARY ---> ", summary_dict)
    return JSONResponse(content=summary_dict)

@app.post("/visualize")
async def visualize(
    filename: str,
    selected_plot: str,
    x: str = None,
    y: str = None
):
    print("VISUALIZE")
    df = pd.read_csv(filename)
    plots = Plots(df)
    plot_dict = {
        "Scatter": plots.scatter_plot,
        "Line": plots.line_plot,
        "Bar": plots.bar_plot,
        "Histogram": plots.histogram_plot,
        "Box": plots.box_plot,
        "Heatmap": plots.heatmap_plot,
        "Pair": plots.pair_plot,
        "Pie": plots.pie_plot
    }
    return JSONResponse(content=plot_dict[selected_plot](x, y))

@app.get("/process_file")
async def process_file():
    return{
        "message": "File received successfully"
    }

if __name__=="__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)