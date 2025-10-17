import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Apple Watch Data Explorer", layout="wide")
st.title("Apple Watch Smart Data Explorer")

@st.cache_data
def read_csv_robust(f):
    try: return pd.read_csv(f)
    except UnicodeDecodeError: return pd.read_csv(f, encoding="latin1")

def clean_columns(df):
    return (df.rename(columns={
        "hear_rate":"heart_rate","entropy_setps":"entropy_steps","norm_heart":"normalized_heart_rate",
        "sd_norm_heart":"sd_normalized_heart_rate","steps_times_distance":"steps_x_distance",
        "Applewatch.Steps_LE":"steps","Applewatch.Heart_LE":"heart_rate",
        "Applewatch.Calories_LE":"calories","Applewatch.Distance_LE":"distance",
        "EntropyApplewatchHeartPerDay_LE":"entropy_heart","EntropyApplewatchStepsPerDay_LE":"entropy_steps",
        "RestingApplewatchHeartrate_LE":"resting_heart","CorrelationApplewatchHeartrateSteps_LE":"corr_heart_steps",
        "NormalizedApplewatchHeartrate_LE":"normalized_heart_rate","ApplewatchIntensity_LE":"intensity_karvonen",
        "StdNormalizedApplewatchHeartrate_LE":"sd_normalized_heart_rate","ApplewatchStepsTimesDistance_LE":"steps_x_distance",
    }).loc[:, ~pd.Index(df.columns).astype(str).str.startswith("Unnamed")])

def coerce_types(df):
    nums = ["age","height","weight","steps","heart_rate","calories","distance","entropy_heart",
            "entropy_steps","resting_heart","corr_heart_steps","normalized_heart_rate",
            "intensity_karvonen","sd_normalized_heart_rate","steps_x_distance"]
    for c in nums:
        if c in df.columns: df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in ["gender","device","activity"]:
        if c in df.columns: df[c] = df[c].astype("category")
    if "gender" in df.columns:
        df["gender"] = df["gender"].replace({0:"Unknown",1:"Male",2:"Female"}).astype("category")
    return df

uploaded = st.file_uploader("Upload CSV (clean or raw)", type=["csv"])
sample = st.toggle("Use sample schema only (no file)?", value=False)

if uploaded or sample:
    df = pd.DataFrame() if sample else read_csv_robust(uploaded)
    if not df.empty or sample:
        df = clean_columns(df); df = coerce_types(df)
        st.subheader("Data Preview")
        st.write(df.head(10))
        st.caption(f"Rows: {len(df):,} | Columns: {len(df.columns)}")

        # Sidebar filters
        st.sidebar.header("Filters")
        if "activity" in df.columns:
            acts = st.sidebar.multiselect("Activity", sorted(df["activity"].dropna().unique().tolist()))
            if acts: df = df[df["activity"].isin(acts)]
        if "device" in df.columns:
            devs = st.sidebar.multiselect("Device", sorted(df["device"].dropna().unique().tolist()))
            if devs: df = df[df["device"].isin(devs)]

        num_cols = [c for c in ["steps","heart_rate","calories","distance",
                                "entropy_heart","entropy_steps","normalized_heart_rate"] if c in df.columns]

        st.subheader("Distributions")
        for c in num_cols:
            fig = plt.figure()
            df[c].dropna().plot(kind="hist", bins=40)
            plt.title(f"Distribution of {c}"); plt.xlabel(c); plt.ylabel("count")
            st.pyplot(fig)

        if "activity" in df.columns:
            st.subheader("By Activity")
            for c in [x for x in ["steps","heart_rate","calories","distance"] if x in df.columns]:
                fig = plt.figure(figsize=(8,4))
                acts = sorted(df["activity"].dropna().unique())
                data = [df[df["activity"]==a][c].dropna().values for a in acts]
                plt.boxplot(data, labels=acts, vert=True, showfliers=False)
                plt.title(f"{c} by Activity"); plt.xlabel("activity"); plt.ylabel(c)
                plt.xticks(rotation=45, ha="right")
                st.pyplot(fig)

        if all(col in df.columns for col in ["steps","heart_rate"]):
            st.subheader("Relationships")
            fig = plt.figure()
            plt.scatter(df["steps"], df["heart_rate"], alpha=0.35)
            plt.title("Heart Rate vs Steps"); plt.xlabel("steps"); plt.ylabel("heart_rate")
            st.pyplot(fig)

        # Auto-insights
        st.subheader("Key Insights")
        insights = []
        if "activity" in df.columns and "steps" in df.columns:
            ts = (df.groupby("activity", observed=True)["steps"].mean()
                    .sort_values(ascending=False).head(3))
            insights.append("Top activities by avg steps: " + ", ".join([f"{i} ({v:.0f})" for i,v in ts.items()]))
        if "activity" in df.columns and "heart_rate" in df.columns:
            thr = (df.groupby("activity", observed=True)["heart_rate"].mean()
                    .sort_values(ascending=False).head(3))
            insights.append("Top activities by avg heart rate: " + ", ".join([f"{i} ({v:.1f} bpm)" for i,v in thr.items()]))
        if all(c in df.columns for c in ["steps","heart_rate"]):
            r = df[["steps","heart_rate"]].dropna().corr().iloc[0,1]
            insights.append(f"Correlation between steps and heart rate: {r:.2f} (Pearson)")
        for s in insights: st.write("•", s)
else:
    st.info("Upload a CSV to get started.")
