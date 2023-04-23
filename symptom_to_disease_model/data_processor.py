import pandas as pd

class DataProcessor:

    def preprocessDiseaseData(self, filename):
        df = pd.read_csv(filename)
        for col in df.columns:
            df[col] = df[col].str.replace('_',' ')
            df[col] = df[col].fillna(0)
        cols = df.columns
        data = df[cols].values.flatten()
        s = pd.Series(data)
        s = s.str.strip()
        s = s.values.reshape(df.shape)
        df = pd.DataFrame(s, columns=df.columns)
        df = df.fillna(0)
        return df

    def readAndProcessSSData(self, filename):
        symptomSeveritydf = pd.read_csv(filename)
        symptomSeveritydf['Symptom'] = symptomSeveritydf['Symptom'].str.replace('_',' ')
        return symptomSeveritydf


    def convertData(self, df, symptomSeveritydf):
            vals = df.values
            symptoms = symptomSeveritydf['Symptom'].unique()
            for i in range(len(symptoms)):
                vals[vals == symptoms[i]] = symptomSeveritydf[symptomSeveritydf['Symptom'] == symptoms[i]]['weight'].values[0]
            d = pd.DataFrame(vals, columns=df.columns)
            d = d.replace('dischromic  patches', 0)
            d = d.replace('spotting  urination',0)
            df = d.replace('foul smell of urine',0)
            return df

dataProcessor  = DataProcessor()