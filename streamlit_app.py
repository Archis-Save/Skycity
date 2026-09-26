import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="SkyCity Auckland Channel Analytics",layout="wide")
st.title("Order Channel Performance & Market Share Analytics")
st.caption("SkyCity Auckland Restaurants & Bars")
@st.cache_data
def load(): return pd.read_csv("SkyCity_Auckland_cleaned.csv")
up=st.sidebar.file_uploader("Upload CSV (optional)",type=["csv"])
df=pd.read_csv(up) if up else load()
orders=["InStoreOrders","UberEatsOrders","DoorDashOrders","SelfDeliveryOrders"]
labels={"InStoreOrders":"In-Store","UberEatsOrders":"Uber Eats","DoorDashOrders":"DoorDash","SelfDeliveryOrders":"Self-Delivery"}
df["AggregatorDependence"]=(df.UberEatsOrders+df.DoorDashOrders)/df.MonthlyOrders
df["ChannelDiversity"]=1-(df[orders].div(df.MonthlyOrders,axis=0)**2).sum(axis=1)
st.sidebar.header("Filters")
def pick(col): return st.sidebar.selectbox(col,["All"]+sorted(df[col].dropna().unique().tolist()))
sub=pick("Subregion"); cuisine=pick("CuisineType"); segment=pick("Segment")
f=df.copy()
if sub!="All": f=f[f.Subregion==sub]
if cuisine!="All": f=f[f.CuisineType==cuisine]
if segment!="All": f=f[f.Segment==segment]
total=f.MonthlyOrders.sum(); mix=f[orders].sum(); mix_share=mix/total
a,b,c,d=st.columns(4)
a.metric("Records",f"{len(f):,}"); b.metric("Monthly orders",f"{total:,.0f}"); c.metric("Aggregator dependence",f"{f.AggregatorDependence.mean():.1%}"); d.metric("Average AOV",f"${f.AOV.mean():.2f}")
t1,t2,t3,t4=st.tabs(["Overview","Geography","Cuisine & Segment","Risk & Economics"])
with t1:
    m=pd.DataFrame({"Channel":[labels[x] for x in mix.index],"Orders":mix.values,"Share":mix_share.values})
    st.plotly_chart(px.bar(m,x="Channel",y="Orders",text=m.Share.map(lambda x:f"{x:.1%}")),use_container_width=True)
    st.dataframe(m.assign(Share=m.Share.map(lambda x:f"{x:.1%}")),hide_index=True)
with t2:
    g=f.groupby("Subregion")[orders].sum().reset_index().melt("Subregion",var_name="Channel",value_name="Orders")
    g["Channel"]=g.Channel.map(labels); g["Share"]=g.Orders/g.groupby("Subregion").Orders.transform("sum")
    st.plotly_chart(px.density_heatmap(g,x="Channel",y="Subregion",z="Share",text_auto=".1%",color_continuous_scale="Blues"),use_container_width=True)
    st.plotly_chart(px.bar(g,x="Subregion",y="Share",color="Channel",barmode="group"),use_container_width=True)
with t3:
    for col in ["CuisineType","Segment"]:
        g=f.groupby(col)[orders].sum().reset_index().melt(col,var_name="Channel",value_name="Orders")
        g["Channel"]=g.Channel.map(labels); g["Share"]=g.Orders/g.groupby(col).Orders.transform("sum")
        st.subheader(col+" vs Channel"); st.plotly_chart(px.bar(g,x=col,y="Share",color="Channel",barmode="stack"),use_container_width=True)
with t4:
    st.metric("Records with ≥70% combined aggregator dependence",int((f.AggregatorDependence>=.70).sum()))
    st.plotly_chart(px.histogram(f,x="AggregatorDependence",nbins=20),use_container_width=True)
    st.plotly_chart(px.scatter(f,x="ChannelDiversity",y="MonthlyOrders",size="AOV",color="Segment",hover_name="RestaurantName"),use_container_width=True)
    rev=f[["InStoreRevenue","UberEatsRevenue","DoorDashRevenue","SelfDeliveryRevenue"]].sum()
    prof=f[["InStoreNetProfit","UberEatsNetProfit","DoorDashNetProfit","SelfDeliveryNetProfit"]].sum()
    e=pd.DataFrame({"Channel":[labels[x] for x in rev.index],"Revenue":rev.values,"Net Profit":prof.values})
    st.dataframe(e.style.format({"Revenue":"${:,.2f}","Net Profit":"${:,.2f}"}),hide_index=True)
