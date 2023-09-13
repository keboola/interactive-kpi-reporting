import pandas as pd
import streamlit as st
import numpy as np
import altair as alt
import src.notifications as ntf
from src.settings import keboola_client
from src.settings import DECIMALS

class KpiComponent():
    def __init__(self, data:pd.DataFrame(), kpi_name:str, agg_function, dto, dfrom, decimals=DECIMALS):
        self.kpi_name = kpi_name
        self.data = data
        self.agg_function = agg_function
        self.dto = dto
        self.dfrom = dfrom
        self.decimals = decimals
        self.subset= pd.DataFrame()
        self.actual = 0
        self.last_planned = 0
        self.client = keboola_client
        self.fill_form()
        
    def select_kpi(self):
        self.subset = self.data.loc[
            (self.data["kpi_name"]==self.kpi_name) & (self.data["date"]>=self.dfrom) & (self.data["date"]<=self.dto)
            ]

        try:
            self.actual = np.round(self.agg_function(
                self.subset["actual_value"]), decimals=self.decimals
                )
            st.write()
            self.last_planned = np.round(self.agg_function(
                self.subset["plan_value"]), decimals=self.decimals
                )
            #self.last_planned = np.round(self.subset["plan_value"].tail(1).values[0], decimals=self.decimals)
        except IndexError:
            st.error("The date range selected does not fit within the data.")
            st.stop()
    
    def create_altair_chart(self):
        ch = alt.Chart(self.subset).mark_line().encode(
            alt.X('date', axis=alt.Axis(title='Date')),
            alt.Y('actual_value', axis=alt.Axis(title='')),
        ) 
        return ch
        
    
    def set_up_message(self):
        base_msg = f"KPI metric: {self.kpi_name} (from {self.dfrom} to {self.dto})."
        base_msg = base_msg + f" Real value: {self.actual}, Planned value: {self.last_planned}. "
        self.base_msg = base_msg + "Comment: "
    
    def fill_form(self):
        self.select_kpi()
        self.set_up_message()
        self.form = st.form(self.kpi_name)
        self.form.metric(self.kpi_name, f"{self.actual} (Real)/ {self.last_planned} (Plan)", np.round(
            self.actual - self.last_planned, decimals=DECIMALS))
        ch = self.create_altair_chart()
        self.form.altair_chart(ch, use_container_width=True)
        slack = self.form.checkbox('Slack')
        with self.form.expander("Notification message"):
            notif = st.text_input(label="Comment", disabled=False)

        send_notif = self.form.form_submit_button("Send Notification")
        if send_notif:
            if slack:
                value = ntf.send_slack_notification(self.client, self.base_msg + notif)
                st.write(f"Slack Notification Status: Table {value}")
