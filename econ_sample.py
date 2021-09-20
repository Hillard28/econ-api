"""Libraries"""
import pandas as pd
import requests
import plotly.express as px
import econ_api

"""FRED sample commands"""
# Create FRED object
fred = econ_api.Fred("!!!Get FRED API key!!!")

# Search FRED for effective federal funds rate time series
search = fred.search_series(search_text="treasury constant maturity rate")

# Create FRED datasets
dgs10 = fred.get_observations(
    series_id="DGS10",
    observation_start="1999-12-31",
    frequency="m",
    aggregation_method="eop",
)
dgs10 = pd.DataFrame(dgs10)
dgs10["date"] = pd.to_datetime(dgs10["date"])
dgs10["value"] = pd.to_numeric(dgs10["value"], errors="coerce")

dgs3mo = fred.get_observations(
    series_id="DGS3MO",
    observation_start="1999-12-31",
    frequency="m",
    aggregation_method="eop",
)
dgs3mo = pd.DataFrame(dgs3mo)
dgs3mo["date"] = pd.to_datetime(dgs3mo["date"])
dgs3mo["value"] = pd.to_numeric(dgs3mo["value"], errors="coerce")

df = pd.concat([dgs10, dgs3mo])


# Plot data with Plotly
fig = px.line(
    df,
    x="date",
    y="value",
    color="id",
    title="United States Treasury Yields",
    labels={"date": "Date", "value": "Yield (%)", "id": "ID"},
    hover_data={"date": "|%B %d, %Y"},
    template="simple_white",
)

fig.update_layout(  # customize font and legend orientation & position
    font_family="Times New Roman",
    title=dict(xref="paper", x=0.5, xanchor="center", font=dict(size=24)),
    legend=dict(
        title=dict(text=None),
        font=dict(size=18),
        orientation="h",
        y=1.0,
        yanchor="bottom",
        x=0.5,
        xanchor="center",
    ),
    margin=dict(l=75, r=25, t=75, b=75),
)

fig.update_xaxes(
    title=dict(text=None, standoff=5, font=dict(size=20)),
    tickfont=dict(size=16),
    tickangle=-45,
    dtick="M24",
)

fig.update_yaxes(title=dict(standoff=5, font=dict(size=20)), tickfont=dict(size=16))

for id in fig.data:
    if id.name == "DGS10":
        id.name = "10-Year"
    elif id.name == "DGS3MO":
        id.name = "3-Month"
recessions = requests.get(
    "https://data.nber.org/data/cycles/business_cycle_dates.json"
).json()

for recession in recessions[1:]:
    if str(min([min(plot.x) for plot in fig.data])) < recession["trough"]:
        if str(min([min(plot.x) for plot in fig.data])) <= recession["peak"]:
            if str(max([max(plot.x) for plot in fig.data])) >= recession["trough"]:
                fig.add_vrect(
                    x0=recession["peak"],
                    x1=recession["trough"],
                    fillcolor="gray",
                    opacity=0.25,
                    line_width=0,
                )
            else:
                fig.add_vrect(
                    x0=recession["peak"],
                    x1=str(max([max(plot.x) for plot in fig.data])),
                    fillcolor="gray",
                    opacity=0.25,
                    line_width=0,
                )
        else:
            if str(max([max(plot.x) for plot in fig.data])) >= recession["trough"]:
                fig.add_vrect(
                    x0=str(min([min(plot.x) for plot in fig.data])),
                    x1=recession["trough"],
                    fillcolor="gray",
                    opacity=0.25,
                    line_width=0,
                )
            else:
                fig.add_vrect(
                    x0=str(min([min(plot.x) for plot in fig.data])),
                    x1=str(max([max(plot.x) for plot in fig.data])),
                    fillcolor="gray",
                    opacity=0.25,
                    line_width=0,
                )
fig.show()

fig.write_image("images/united_states_treasury_yields_px.svg", width=800, height=600)
fig.write_html("images/united_states_treasury_yields_interactive.html", auto_open=True)


"""Census sample commands"""
# Create census object
# census = census_api.Census('!!!use Census API key here!!!')
census = econ_api.Census("!!!Optional: get Census API key!!!")

# Create dictionary
dict_acs5 = census.get_dict(source="acs5", year="2019")

# Creates acs datasets
acs2019 = census.get_data(
    source="acs5",
    year="2019",
    variables=["B03001_003E", "NAME"],
    geographical_level="county",
)

# Create dataframe
df_acs2019 = pd.DataFrame(acs2019)
df_acs2019["B03001_003E"] = pd.to_numeric(df_acs2019["B03001_003E"], errors="coerce")
df_acs2019[df_acs2019["B03001_003E"] < 0] = pd.NA

df_acs2019["FIPS"] = df_acs2019["state"] + df_acs2019["county"]
