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
        req='https://data.sfgov.org/resource/6h2p-rdar.json?$select=estimated_contents_loss,estimated_property_loss,alarm_dttm,arrival_dttm,fire_fatalities,fire_injuries,civilian_fatalities,civilian_injuries,neighborhood_district&$limit=50000&$offset='+str(x)
        js=requests.get(req).json()
        j.append(js)
        x+=50000
    print('Charged '+str(total)+' registers!')
    return j


class Incident:
    def __init__(self):
        self.resources=getResources()
    def timeXloss(self):
        j=self.resources
        response1=""
        
        for x in range(len(j)):
            count=0
            for y in j[x]:
               if len(str(y.get('alarm_dttm')).split('T'))>1:
                if len(str(y.get('arrival_dttm')).split('T'))>1:
                   t= diff_times_in_seconds(str(y.get('alarm_dttm')).split('T')[1], str(y.get('arrival_dttm')).split('T')[1])
               else:
                   t=0
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
               l=p+c
               if t>0:    
                response1+='['+str(abs(t))+','+str(abs(l))+']'
       
                if(count<=len(j[x])): 
                 response1+=','
                count=count+1
        s=''
        response1.split(']')[len(response1.split(']'))-1]=s
        return response1


    
        
    def timeXVictims(self):
        j=self.resources
        response2=""
        
        for x in range(len(j)):
            count=0
            for y in j[x]:
               if len(str(y.get('alarm_dttm')).split('T'))>1:
                if len(str(y.get('arrival_dttm')).split('T'))>1:
                   t= diff_times_in_seconds(str(y.get('alarm_dttm')).split('T')[1], str(y.get('arrival_dttm')).split('T')[1])
               else:
                   t=0
               ff=0
               fi=0
               cf=0
               ci=0
               if(y.get('fire_fatalities')==None):
                   pass
               if(y.get('fire_injuries')==None):
                   pass
               if(y.get('civilian_fatalities')==None):
                   pass
               if(y.get('civilian_injuries')==None):
                   pass
               if(y.get('fire_fatalities')>=0):
                    ff=int(y.get('fire_fatalities'))
               if(y.get('fire_injuries')>=0):
                    fi=int(y.get('fire_injuries'))
               if(y.get('civilian_fatalities')>=0):
                    cf=int(y.get('civilian_fatalities'))
               if(y.get('civilian_injuries')>=0):
                   ci=int(y.get('civilian_injuries'))
               v=ff+fi+cf+ci
               if t>0:    
                response2+='['+str(abs(t))+','+str(abs(v))+']'
       
                if(count<len(j[x])): 
                 response2+=','
               count=count+1

        del(response2.split(']')[len(response2.split(']'))-1])
        return response2
    @staticmethod
    def returnIncidents():
        i=Incident()
        d={'loss':i.timeXloss(),'victims':i.timeXVictims()}
        return d


def neighborhoodxfireincident():
    response='["Neighborhood District", "Number of incidents", { role: "style" } ],'    
    req='https://data.sfgov.org/resource/6h2p-rdar.json?$select=neighborhood_district,COUNT(incident_number)&$group=neighborhood_district'
    js=requests.get(req).json()
    for x in range(len(js)-2):
        response+='["'+str(js[x].get('neighborhood_district'))+'",'+str(js[x].get('count_incident_number'))+',"'+str("#%06x" % random.randint(0, 0xFFFFFF))+'"],'
    response+='["'+str(js[len(js)-1].get('neighborhood_district'))+'",'+str(js[len(js)-1].get('count_incident_number'))+',"'+str("#%06x" % random.randint(0, 0xFFFFFF))+'"]'
    return response



