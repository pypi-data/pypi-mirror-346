import pandas as pd
import os
import numpy as np
from datetime import timedelta
from datupapi.utils.utils import Utils
from datupapi.inventory.src.SuggestedForecast.suggested_forecast import SuggestedForecast
from datupapi.inventory.src.FutureInventory.daily_usage_future import DailyUsageFuture


class FutureReorder():

    def __init__(self, df_inv, df_lead_time, df_prep, df_fcst, periods, start_date, location=False, security_stock_ref=False):
        self.df_inv = df_inv
        self.df_lead_time = df_lead_time        
        self.df_prep = df_prep
        self.df_fcst = df_fcst
        self.default_coverage = 30
        self.periods = periods
        self.start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
        self.location = location
        self.security_stock_ref = security_stock_ref


    def future_date(self):

        '''Function to calculate the future dates by Item or Item-Location'''

        DOCKER_CONFIG_PATH = os.path.join('/opt/ml/processing/input', 'config.yml')
        utils = Utils(config_file=DOCKER_CONFIG_PATH, logfile='data_io', log_path='output/logs')

        timestamp = utils.set_timestamp()
        actual_date = pd.to_datetime(str(int(float(timestamp[0:8]))), format='%Y%m%d')

        item_dates = {}

        columns = ['Item', 'ReorderFreq']
        if self.location:
            columns.append('Location')

        for _, row in self.df_lead_time[columns].drop_duplicates().iterrows():
            item = row['Item']
            location = row['Location'] if self.location else None
            cobertura = int(row['ReorderFreq']) if not pd.isnull(row['ReorderFreq']) and row['ReorderFreq'] != 0 else self.default_coverage
            date = self.start_date
            dates = []

            while date <= actual_date + pd.DateOffset(months=self.periods):
                dates.append(date.strftime('%Y%m%d'))
                date += timedelta(days=cobertura)

            item_dates[(item, location) if self.location else item] = dates

        return item_dates


    def reorder(self):

        '''Function to calculate the future reorder for inventory with dynamics coverage'''

        item_dates = self.future_date()

        metadata = ['Item']
        if self.location:
            metadata.append('Location')

        df_lead_time_rf = self.df_lead_time.copy()
        df_lead_time_rf['Coverage'] = df_lead_time_rf['ReorderFreq']    
        df_lead_time_rf['AvgLeadTime'] = df_lead_time_rf['ReorderFreq']
        df_lead_time_rf['MaxLeadTime'] = df_lead_time_rf['ReorderFreq']

        SuggestedForecast_cov = {}
        SuggestedForecast_rf = {}
        df_forecast = {}
        df_avg_gen = {}
        df_max_gen = {}
        df_sstock = {}
        df_inventory = {}
        df = {}

        # Inicializar DataFrame
        columns = ['Date', 'Item'] + (['Location'] if self.location else [])
        data_frame = pd.DataFrame(columns=columns)

        # Iterar por cada combinación (Item, Location) o (Item) según use_location
        for key, dates in item_dates.items():
            if self.location:
                item, location = key
            else:
                item = key
                location = None

            for i, date in enumerate(dates):
                if self.location:
                    current_df_lead_time_cov = self.df_lead_time[(self.df_lead_time['Item'] == item) &
                                                            (self.df_lead_time['Location'] == location)]

                    current_df_lead_time_rf = df_lead_time_rf[(df_lead_time_rf['Item'] == item) &
                                                            (df_lead_time_rf['Location'] == location)]

                    current_df_inv = self.df_inv[(self.df_inv['Item'] == item) &
                                                (self.df_inv['Location'] == location)]

                else:
                    current_df_lead_time_cov = self.df_lead_time[self.df_lead_time['Item'] == item]
                    current_df_lead_time_rf = df_lead_time_rf[df_lead_time_rf['Item'] == item]
                    current_df_inv = self.df_inv[self.df_inv['Item'] == item]
                    
                if current_df_lead_time_cov.empty or current_df_lead_time_rf.empty or current_df_inv.empty:                    
                    continue

                # SuggestedForecast_Coverage
                SuggestedForecast_cov[i] = SuggestedForecast(df_LeadTimes=current_df_lead_time_cov,
                                                            df_Forecast=self.df_fcst,
                                                            df_Prep=self.df_prep,
                                                            df_inv=current_df_inv,
                                                            column_forecast='SuggestedForecast',
                                                            columns_metadata=metadata,
                                                            frequency_='M',
                                                            location=self.location,
                                                            actualdate=date,
                                                            default_coverage_=self.default_coverage,
                                                            join_='left').suggested_forecast()
                
                SuggestedForecast_cov[i].rename(columns={'SuggestedForecast':'Suggested_Coverage'},inplace=True)
                                
                # SuggestedForecast_ReorderFreq
                SuggestedForecast_rf[i] = SuggestedForecast(df_LeadTimes=current_df_lead_time_rf,
                                                            df_Forecast=self.df_fcst,
                                                            df_Prep=self.df_prep,
                                                            df_inv=current_df_inv,
                                                            column_forecast='SuggestedForecast',
                                                            columns_metadata=metadata,
                                                            frequency_='M',
                                                            location=self.location,
                                                            actualdate=date,
                                                            default_coverage_=self.default_coverage,
                                                            join_='left').suggested_forecast()
    
                SuggestedForecast_rf[i].rename(columns={'SuggestedForecast':'Suggested_ReorderFreq'},inplace=True)
                SuggestedForecast_rf[i] = SuggestedForecast_rf[i][metadata + ['Suggested_ReorderFreq']]

                # Concatenar                                
                df_forecast[i] = pd.merge(SuggestedForecast_cov[i], SuggestedForecast_rf[i], on=metadata, how='outer')                
                
                # Calcular AvgDailyUsage y MaxDailyUsage
                df_avg_gen[i] = DailyUsageFuture(location=self.location,
                                                  column_forecast='SuggestedForecast',
                                                  date=date,
                                                  df_fcst=self.df_fcst).daily_usage(df_forecast[i], 'AvgDailyUsage').fillna(0)

                df_max_gen[i] = DailyUsageFuture(location=self.location,
                                                  column_forecast='SuggestedForecast',
                                                  date=date,
                                                  df_fcst=self.df_fcst).daily_usage(df_avg_gen[i], 'MaxDailyUsage').fillna(0)

                #Ajustar AvgDailyUsage y MaxDailyUsage si es cero.
                df_avg_gen[i] = df_avg_gen[i].replace(0,0.001)
                df_max_gen[i] = df_max_gen[i].replace(0,0.0012)                
 
                # Calcular Stock de Seguridad
                merge_columns = ['Item', 'Location', 'AvgLeadTime', 'MaxLeadTime'] if self.location else ['Item', 'AvgLeadTime', 'MaxLeadTime']
                df_sstock[i] = pd.merge(df_max_gen[i], current_df_lead_time_cov[merge_columns], on=metadata, how='inner').drop_duplicates()

                # Current Period
                if i == 0:
                    inventory_columns = ['Item', 'Location', 'Inventory', 'Transit', 'PurchaseFactor'] if self.location else ['Item', 'Inventory', 'Transit', 'PurchaseFactor']
                    df_inventory[i] = current_df_inv[inventory_columns]
                    df_inventory[i]['InventoryTransit'] = df_inventory[i]['Inventory'] + df_inventory[i]['Transit']
                    df_inventory[i] = df_inventory[i][metadata + ['InventoryTransit']]
                    df[i] = pd.merge(df_inventory[i], df_sstock[i], on=metadata, how='inner')
         
                    if self.security_stock_ref:
                        df[i]['SecurityStock'] = df[i]['SecurityStockDaysRef'] * df[i]['AvgDailyUsage']
                    else:
                        df[i]['SecurityStock'] = (df[i]['MaxDailyUsage'] * df[i]['MaxLeadTime']) - (df[i]['AvgDailyUsage'] * df[i]['AvgLeadTime'])

                    df[i]['ReorderPoint'] = (df[i]['Suggested_Coverage'] + df[i]['SecurityStock']).clip(lower=0)
                    df[i]['ReorderQtyBase'] = (df[i]['ReorderPoint'] - df[i]['InventoryTransit']).clip(lower=1)
                    df[i]['ReorderQty'] = ((df[i]['ReorderQtyBase'] / df[i]['PurchaseFactor']).apply(np.ceil)) * df[i]['PurchaseFactor']
                    df[i]['ReorderQtyDays'] = (df[i]['ReorderQty'] / df[i]['AvgDailyUsage']).astype(int)
                    
                # Future Dates
                else:
                    inventory_columns = ['Item', 'Location', 'PurchaseFactor'] if self.location else ['Item', 'PurchaseFactor']
                    df_inventory[i] = current_df_inv[inventory_columns]
                    df[i] = pd.merge(df_inventory[i], df_sstock[i], on=inventory_columns, how='inner')

                    if self.security_stock_ref:
                        df[i]['SecurityStock'] = df[i]['SecurityStockDaysRef'] * df[i]['AvgDailyUsage']
                    else:
                        df[i]['SecurityStock'] = (df[i]['MaxDailyUsage'] * df[i]['MaxLeadTime']) - (df[i]['AvgDailyUsage'] * df[i]['AvgLeadTime'])

                    df[i]['InventoryTransit'] = ((df[i-1]['InventoryTransit'] - df[i-1]['Suggested_ReorderFreq']) + df[i-1]['ReorderQty']).clip(lower=0)
                    df[i]['ReorderPoint'] = (df[i]['Suggested_Coverage'] + df[i]['SecurityStock']).clip(lower=0)
                    df[i]['ReorderQtyBase'] = (df[i]['ReorderPoint'] - df[i]['InventoryTransit']).clip(lower=1)
                    df[i]['ReorderQty'] = ((df[i]['ReorderQtyBase'] / df[i]['PurchaseFactor']).apply(np.ceil)) * df[i]['PurchaseFactor']
                    df[i]['ReorderQtyDays'] = (df[i]['ReorderQty'] / df[i]['AvgDailyUsage']).astype(int)
                    

                # Insert columns
                df[i].insert(loc=0, column='Date', value=date)
                df[i]['Item'] = item
                
                if self.location:
                    df[i]['Location'] = location

                data_frame = pd.concat([data_frame, df[i]], ignore_index=True)

                # Final DataFrame
                leadtimes_columns = ['Item', 'Location', 'ReorderFreq', 'Coverage'] if self.location else ['Item', 'ReorderFreq', 'Coverage']
                leadtimes = self.df_lead_time[leadtimes_columns]
                df_final = pd.merge(data_frame, leadtimes, on=metadata, how='left').fillna(0)

                df_final['Date'] = pd.to_datetime(df_final['Date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
                df_final = df_final.rename(columns={'InventoryTransit': 'FutureInventory'})                
                cols_to_round = ['SecurityStock', 'FutureInventory', 'Suggested_Coverage', 'Suggested_ReorderFreq', 'ReorderPoint', 'ReorderQtyBase']
                df_final[cols_to_round] = df_final[cols_to_round].apply(np.ceil)
                final_cols = ['Date', 'Item', 'ItemDescription', 'Location', 'Suggested_Coverage', 'Suggested_ReorderFreq', 'FutureInventory', 'ReorderQtyBase', 'ReorderQty', 'ReorderQtyDays', 'PurchaseFactor', 'ReorderPoint', 'SecurityStock',
                              'AvgDailyUsage', 'MaxDailyUsage', 'AvgLeadTime', 'MaxLeadTime', 'ReorderFreq', 'Coverage'] if self.location \
                              else ['Date', 'Item', 'ItemDescription', 'Suggested_Coverage', 'Suggested_ReorderFreq', 'FutureInventory', 'ReorderQtyBase', 'ReorderQty', 'ReorderQtyDays', 'PurchaseFactor', 'ReorderPoint', 'SecurityStock',
                              'AvgDailyUsage', 'MaxDailyUsage', 'AvgLeadTime', 'MaxLeadTime', 'ReorderFreq', 'Coverage']
                df_final = df_final[final_cols]

        return df_final