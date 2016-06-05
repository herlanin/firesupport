"""
Definition of models.
"""

from django.db import models
import simplejson
import urllib2
import requests
from datetime import datetime
import time
import random

def diff_times_in_seconds(t1, t2):
    # caveat emptor - assumes t1 & t2 are python times, on the same day and t2 is after t1
    t1 = time.strptime(t1, '%H:%M:%S')
    t2 = time.strptime(t2, '%H:%M:%S')
    h1, m1, s1 = t1.tm_hour, t1.tm_min, t1.tm_sec
    h2, m2, s2 = t2.tm_hour, t2.tm_min, t2.tm_sec
    t1_secs = s1 + 60 * (m1 + 60*h1)
    t2_secs = s2 + 60 * (m2 + 60*h2)
    return( t2_secs - t1_secs)
#Columns
 #incident_number text Incident Number
 #exposure_number number Exposure Number
 #address text Address
 #incident_date floating_timestamp Incident Date
 #call_number text Call Number
 #alarm_dttm floating_timestamp Alarm DtTm
 #arrival_dttm floating_timestamp Arrival DtTm
 #close_dttm floating_timestamp Close DtTm
 #city text City
 #zipcode text Zipcode
 #battalion text Battalion
 #station_area text Station Area
 #box text Box
 #suppression_units number Suppression Units
 #suppression_personnel number Suppression Personnel
 #ems_units number EMS Units
 #ems_personnel number EMS Personnel
 #other_units number Other Units
 #other_personnel number Other Personnel
 #first_unit_on_scene text First Unit On Scene
 #estimated_property_loss number Estimated Property Loss
 #estimated_contents_loss number Estimated Contents Loss
 #fire_fatalities number Fire Fatalities
 #fire_injuries number Fire Injuries
 #civilian_fatalities number Civilian Fatalities
 #civilian_injuries number Civilian Injuries
 #number_of_alarms number Number of Alarms
 #primary_situation text Primary Situation
 #mutual_aid text Mutual Aid
 #action_taken_primary text Action Taken Primary
 #action_taken_secondary text Action Taken Secondary
 #action_taken_other text Action Taken Other
 #detector_alerted_occupants text Detector Alerted Occupants
 #property_use text Property Use
 #area_of_fire_origin text Area of Fire Origin
 #ignition_cause text Ignition Cause
 #ignition_factor_primary text Ignition Factor Primary
 #ignition_factor_secondary text Ignition Factor Secondary
 #heat_source text Heat Source
 #item_first_ignited text Item First Ignited
 #human_factors_associated_with_ignition text Human Factors Associated with Ignition
 #structure_type text Structure Type
 #structure_status text Structure Status
 #floor_of_fire_origin number Floor of Fire Origin
 #fire_spread text Fire Spread
 #no_flame_spead text No Flame Spead
 #number_of_floors_with_minimum_damage number Number of floors with minimum damage
 #number_of_floors_with_significant_damage text Number of floors with significant damage
 #number_of_floors_with_heavy_damage number Number of floors with heavy damage
 #number_of_floors_with_extreme_damage number Number of floors with extreme damage
 #detectors_present text Detectors Present
 #detector_type text Detector Type
 #detector_operation text Detector Operation
 #detector_effectiveness text Detector Effectiveness
 #detector_failure_reason text Detector Failure Reason
 #automatic_extinguishing_system_present text Automatic Extinguishing System Present
 #automatic_extinguishing_sytem_type text Automatic Extinguishing Sytem Type
 #automatic_extinguishing_sytem_perfomance text Automatic Extinguishing Sytem Perfomance
 #automatic_extinguishing_sytem_failure_reason text Automatic Extinguishing Sytem Failure Reason
 #number_of_sprinkler_heads_operating number Number of Sprinkler Heads Operating
 #supervisor_district text Supervisor District
 #neighborhood_district text Neighborhood District
 #location_city text Location (city)
 #location point Location
 #location_address text Location (address)
 #location_zip text Location (zip)
 #location_state text Location (state)

    #--------------------------GET TOTAL---------------------------------------
def total():
    totalurl='https://data.sfgov.org/resource/6h2p-rdar.json?$select=count(incident_number)'
    totalj=requests.get(totalurl).json()
    total=int(totalj[0].get('count_incident_number'))
    return total
__TOTAL__=total()
#--------------------------GET RESOURCES---------------------------------------
def getResources():
    total=__TOTAL__
    x=0
    dataList=[]
    print('charging data...')
    parts=str(total//50000)
    j=[]
    while x<total:
        print('part '+str(x//50000)+ ' of ' + parts)
        req='https://data.sfgov.org/resource/6h2p-rdar.json?$select=estimated_contents_loss,estimated_property_loss,alarm_dttm,arrival_dttm,neighborhood_district&$limit=50000&$offset='+str(x)
        js=requests.get(req).json()
        j.append(js)
        x+=50000
    print('Charged '+str(total)+' registers!')
    return j

class Inc:
    def __init__(self):
        self.time=0
        self.loss=0
class Resource:
    def __init__(self):
        self.resources=getResources()

    def timeXloss(self):
        j=self.resources
        response=""
        li=[]
        for x in range(len(j)):
            count=0
            
            for y in j[x]:
               i=Inc()
               if len(str(y.get('alarm_dttm')).split('T'))>1:
                if len(str(y.get('arrival_dttm')).split('T'))>1:
                   t= diff_times_in_seconds(str(y.get('alarm_dttm')).split('T')[1], str(y.get('arrival_dttm')).split('T')[1])
                   i.time=abs(t)
               else:
                t=0
                i.time=t
               c=0
               p=0
               if(y.get('estimated_contents_loss')==None):
                   pass
               if(y.get('estimated_property_loss')==None):
                   pass
               if(y.get('estimated_contents_loss')>=0):
                    c=int(y.get('estimated_contents_loss'))
               if(y.get('estimated_property_loss')>=0):
                   p=int(y.get('estimated_property_loss'))
               l=abs(p)+abs(c)
               i.loss=l
               if t>0 and t<1000:    
                li.append(i)
        
        li.sort(key=lambda i:i.time, reverse=False)
        for x in range(len(li)-2):
            response+='['+str(li[x].time)+','+str(li[x].loss)+'],'
        response+='['+str(li[len(li)-1].time)+','+str(li[len(li)-1].loss)+']'
        return response
    def neighborhoodxfireincident(self):
        response='["Neighborhood District", "Number of incidents", { role: "style" } ],'    
        req='https://data.sfgov.org/resource/6h2p-rdar.json?$select=neighborhood_district,COUNT(incident_number)&$group=neighborhood_district&$order=neighborhood_district'
        js=requests.get(req).json()
        for x in range(len(js)-2):
            response+='["'+str(js[x].get('neighborhood_district'))+'",'+str(js[x].get('count_incident_number'))+',"'+str("#%06x" % random.randint(0, 0xFFFFFF))+'"],'
        response+='["'+str(js[len(js)-1].get('neighborhood_district'))+'",'+str(js[len(js)-1].get('count_incident_number'))+',"'+str("#%06x" % random.randint(0, 0xFFFFFF))+'"]'
        return response

    def averageLossesNeighborhood(self):
        response='["Neighborhood District", "AVG Losses", { role: "style" } ],'
        reqc='https://data.sfgov.org/resource/6h2p-rdar.json?$select=neighborhood_district,AVG(estimated_contents_loss)%20as%20avgCloss&$group=neighborhood_district&$order=neighborhood_district'

        reqp='https://data.sfgov.org/resource/6h2p-rdar.json?$select=neighborhood_district,AVG(estimated_property_loss)%20as%20avgPloss&$group=neighborhood_district&$order=neighborhood_district'
        js=requests.get(reqc).json()
        js2=requests.get(reqp).json()

        for x in range(len(js)-2):
            response+='["'+str(js[x].get('neighborhood_district'))+'",'+str(round((float(js[x].get('avgcloss'))+float(js2[x].get('avgploss'))),2))+',"'+str("#%06x" % random.randint(0, 0xFFFFFF))+'"],'
        response+='["'+str(js[len(js)-1].get('neighborhood_district'))+'",'+str(round((float(js[len(js)-1].get('avgcloss'))+float(js2[len(js)-1].get('avgploss'))),2))+',"'+str("#%06x" % random.randint(0, 0xFFFFFF))+'"]'
        return response

    def normalLosses(self):
   
        req='https://data.sfgov.org/resource/6h2p-rdar.json?$select=incident_number,estimated_property_loss,estimated_contents_loss&$limit=50000&$order=estimated_property_loss*estimated_contents_loss'
        js=requests.get(req).json()
        response='["Incident Number", "Losses"],'
        for x in range(len(js)-2):
            c=0
            p=0
            if(js[x].get('estimated_contents_loss')==None):
                pass
            if(js[x].get('estimated_property_loss')==None):
                pass
            if(js[x].get('estimated_contents_loss')>=0):
                c=float(js[x].get('estimated_contents_loss'))
            if(js[x].get('estimated_property_loss')>=0):
                p=float(js[x].get('estimated_property_loss'))
            l=abs(p)+abs(c)
            response+='["'+str(js[x].get('incident_number'))+'",'+str(l)+'],'
        c=0
        p=0
        if(js[len(js)-1].get('estimated_contents_loss')==None):
            pass
        if(js[len(js)-1].get('estimated_property_loss')==None):
            pass
        if(js[len(js)-1].get('estimated_contents_loss')>=0):
            c=float(js[len(js)-1].get('estimated_contents_loss'))
        if(js[len(js)-1].get('estimated_property_loss')>=0):
            p=float(js[len(js)-1].get('estimated_property_loss'))
        l=abs(p)+abs(c)
        response+='["'+str(js[len(js)-1].get('incident_number'))+'",'+str(l)+']'
        return response



    def incidentsXLosses(self):
   
        numIncNeighREQ='https://data.sfgov.org/resource/6h2p-rdar.json?$select=neighborhood_district,COUNT(incident_number)&$group=neighborhood_district&$order=neighborhood_district'

        reqc='https://data.sfgov.org/resource/6h2p-rdar.json?$select=neighborhood_district,AVG(estimated_contents_loss)%20as%20avgCloss&$group=neighborhood_district&$order=neighborhood_district'

        reqp='https://data.sfgov.org/resource/6h2p-rdar.json?$select=neighborhood_district,AVG(estimated_property_loss)%20as%20avgPloss&$group=neighborhood_district&$order=neighborhood_district'
        js=requests.get(numIncNeighREQ).json()
        js2=requests.get(reqc).json()
        js3=requests.get(reqp).json()
        response='["Neighborhood District", "AVG Losses x Occurencies", { role: "style" } ],'

        for x in range(len(js)-2):
            response+='["'+str(js[x].get('neighborhood_district'))+'",'+str(round((float(js2[x].get('avgcloss'))+float(js3[x].get('avgploss')))*int(js[x].get('count_incident_number')),2))+',"'+str("#%06x" % random.randint(0, 0xFFFFFF))+'"],'
        response+='["'+str(js[len(js)-1].get('neighborhood_district'))+'",'+str(round((float(js2[len(js)-1].get('avgcloss'))+float(js3[len(js)-1].get('avgploss')))*int(js[len(js)-1].get('count_incident_number')),2))+',"'+str("#%06x" % random.randint(0, 0xFFFFFF))+'"]'
        return response
    @staticmethod
    def returnResources():
        r=Resource()
        d={'timeXloss':r.timeXloss(),'averageLossesNeighborhood':r.averageLossesNeighborhood(),'incidentsXLosses':r.incidentsXLosses(),'neighborhoodxfireincident':r.neighborhoodxfireincident(),'normalLosses':r.normalLosses()}
        return d






