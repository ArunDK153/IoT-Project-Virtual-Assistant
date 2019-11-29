#include "ThingSpeak.h"
#include <ESP8266WiFi.h>
#include<Servo.h>


//----------------  Fill in your credentails   ---------------------
char ssid[] = "Hogwarts_WiFi";     // your network SSID (name) 
char pass[] = "JKRowling"; // your network password
//------------------------------------------------------------------

Servo myservo;
Servo myservo1;
WiFiClient  client;
int led1pin=11;
int led2pin=12;
int led3pin=13;
int tempinputpin=A0;
int ldrpin=A1;


unsigned long CcodeChannelNumber = 917355;
unsigned int  CcFieldNumber = 1;
unsigned long statusChannelNumber = 917359;
unsigned int  statusled1FieldNumber = 1;
unsigned int  statusled2FieldNumber = 2;
unsigned int  statusled3FieldNumber = 3;
unsigned int  statusfanFieldNumber = 4;
unsigned int  statusautoled1FieldNumber = 5;
unsigned int  statusautoled2FieldNumber = 6;
unsigned int  statusautoled3FieldNumber = 7;
unsigned int  statusautofanFieldNumber = 8;
unsigned long tempChannelNumber = 917357;
unsigned int  tempFieldNumber = 1;
unsigned long ldrChannelNumber = 917360;
unsigned int  ldrFieldNumber = 1;

const char* readccAPIKey = "4QWRT1OID7P3AOH6";
const char* writeccAPIKey = "U6DEUI2SRWRL9WHW";
const char* readstatusAPIKey = "CU4W1P240POXKOQP";
const char* writestatusAPIKey = "D0NHX0U06GF6S07Y";
const char* readtempAPIKey = "5DN1YXKWR7WSVZCR";
const char* writetempAPIKey = "OKVY8C07ULV7952P";
const char* readldrAPIKey = "U141VNK3E5WV5U2Z";
const char* writeldrAPIKey = "YDPG4M2LWQ56K70C";

int flagled1=0;
int flagled2=0;
int flagled3=0;
int flagfan=0;


void setup() 
{
 // Initialize serial and wait for port to open:
 // while (!Serial) {
 // wait for serial port to connect. Needed for native USB port only
 // }
 myservo.attach(10);
 myservo1.attach(3);
 pinMode(3,OUTPUT);
 pinMode(led1pin,OUTPUT);
 pinMode(led2pin,OUTPUT);
 pinMode(led3pin,OUTPUT);
 pinMode(tempinputpin,INPUT);
 pinMode(ldrpin,INPUT);
 Serial.begin(115200);
 WiFi.mode(WIFI_STA); 
 WiFi.begin(ssid, pass);
 if(WiFi.status() != WL_CONNECTED)
 {
   Serial.print("Attempting to connect to SSID: ");
   Serial.println(ssid);
   while(WiFi.status() != WL_CONNECTED)
   {
     Serial.print(".");
     delay(500);     
   } 
   Serial.println("\nConnected");
 } 
 ThingSpeak.begin(client);
 
}

void loop() {

 int constatusCode1 = 0;    //is checked after reading from cloud 
 int constatuscode2=0;      //is checked after writing to cloud
 // Read in field 4 of the public channel recording the temperature
int Controlcode = 103;//ThingSpeak.readIntField(CcodeChannelNumber,CcFieldNumber,readccAPIKey);
  
//String temperatureInF = ThingSpeak.readStringField(weatherStationChannelNumber,temperatureFieldNumber,readAPIKey);  

constatusCode1 = ThingSpeak.getLastReadStatus();

 // Check the status of the read operation to see if it was successful
 
if(constatusCode1 == 200)
{
    if(flagled1==1)
    {
      digitalWrite(led1pin,HIGH);
       delay(1000);
       Serial.println("Led1 on");
    }
    else
    {   digitalWrite(led1pin,LOW);
       delay(1000);
       Serial.println("Led1 off");
    }
    if(flagled2==1)
    {   digitalWrite(led2pin,HIGH);
       delay(1000);
       Serial.println("Led2 on");
    }
    else
    {   digitalWrite(led2pin,LOW);
       delay(1000);
       Serial.println("Led2 off");
    }
    if(flagled3==1)
    {
      digitalWrite(led3pin,HIGH);
       delay(1000);
       Serial.println("Led3 on");
    }
    else
     {  digitalWrite(led3pin,LOW);
       delay(1000);
       Serial.println("Led3 off");
     }
    if(flagfan==1)
       {
            for(int pos=0;pos<=180;pos+=10)
            {
               myservo.write(pos);
               delay(10);
            }
            for(int pos=180;pos<=0;pos-=10)
            {
               myservo.write(pos);
               delay(10);
            }
       }
    else
    {
      myservo.write(0);
      delay(1000);
    }
}

    if(Controlcode==110)
    {
      Serial.println("yes");
      constatuscode2=ThingSpeak.writeField(  statusChannelNumber,statusautoled1FieldNumber,1,writestatusAPIKey);
      int threshold=500;
     float sensedvalue=analogRead(ldrpin);

      if(constatuscode2!=200)
        {
           Serial.println("Error updating status to cloud. Error code: ");
           Serial.print(constatuscode2);
        }
      else 
        {
          if(sensedvalue>threshold)
            {
                digitalWrite(led1pin,LOW);
                flagled1=0;
                delay(1000);
    ThingSpeak.writeField(statusChannelNumber,statusled1FieldNumber,0,writestatusAPIKey);
    delay(1000);
    Serial.println("Living room light turned off.");
            }
           else if(sensedvalue<=threshold)
            {
                digitalWrite(led1pin,HIGH);
                flagled1=1;
                delay(1000);
    ThingSpeak.writeField(statusChannelNumber,statusled1FieldNumber,1,writestatusAPIKey);
    delay(1000);
    Serial.println("Living room light turned on.");                
            }

        }
    }
else if(Controlcode==111)
    {
      constatuscode2=ThingSpeak.writeField(  statusChannelNumber,statusautoled2FieldNumber,1,writestatusAPIKey);
      int threshold=500;
      float sensedvalue=analogRead(ldrpin);

      if(constatuscode2!=200)
        {
           Serial.println("Error updating status to cloud. Error code: ");
           Serial.print(constatuscode2);
        }
      else 
        {
          if(sensedvalue>threshold)
            {
                digitalWrite(led2pin,LOW);
                flagled2=0;
                delay(1000);
                ThingSpeak.writeField(statusChannelNumber,statusled2FieldNumber,0,writestatusAPIKey);
    delay(1000);
    Serial.println("Bed room light turned off.");
            }
           else if(sensedvalue<=threshold)
            {
                digitalWrite(led2pin,HIGH);
                flagled2=1;
                delay(1000);  
                ThingSpeak.writeField(statusChannelNumber,statusled2FieldNumber,1,writestatusAPIKey);
    delay(1000);
    Serial.println("Bed room light turned on.");                
            }

        }
    }
else if(Controlcode==112)
    {
      constatuscode2=ThingSpeak.writeField(  statusChannelNumber,statusautoled3FieldNumber,1,writestatusAPIKey);
      int threshold=500;
    float  sensedvalue=analogRead(ldrpin);

      if(constatuscode2!=200)
        {
           Serial.println("Error updating status to cloud. Error code: ");
           Serial.print(constatuscode2);
        }
      else 
        {
          if(sensedvalue>threshold)
            {
                digitalWrite(led3pin,LOW);
                flagled3=0;
                delay(1000);
                ThingSpeak.writeField(statusChannelNumber,statusled3FieldNumber,0,writestatusAPIKey);
    delay(1000);
    Serial.println("Dining room light turned off.");
            }
           else if(sensedvalue<=threshold)
            {
                digitalWrite(led3pin,HIGH);
                flagled3=1;
                delay(1000);
                ThingSpeak.writeField(statusChannelNumber,statusled3FieldNumber,1,writestatusAPIKey);
    delay(1000);
    Serial.println("Dining room light turned on.");                
            }

        }
    }
 else if(Controlcode==101)
     {         Serial.println("yes");
               constatuscode2=ThingSpeak.writeField( statusChannelNumber,statusled1FieldNumber,1,writestatusAPIKey);
               if(constatuscode2!=200)
                  {
               Serial.println("Error updating status to cloud. Error code: ");
               Serial.print(constatuscode2);
                  }
               else
                 {
                    digitalWrite(led1pin,HIGH);
                    delay(1000);
                    Serial.println("Living room light is on");
                    flagled1=1;
                 }
     }
    else if(Controlcode==102)
      {
               constatuscode2=ThingSpeak.writeField( statusChannelNumber,statusled2FieldNumber,1,writestatusAPIKey);
               if(constatuscode2!=200)
                  {
               Serial.println("Error updating status to cloud. Error code: ");
               Serial.print(constatuscode2);
                  }
               else
                 {
                    digitalWrite(led2pin,HIGH);
                     delay(1000);
                    Serial.println("Bedroom light is on");
                    flagled2=1;
                 }      
      }
      else if(Controlcode==103)
      {
               constatuscode2=ThingSpeak.writeField( statusChannelNumber,statusled3FieldNumber,1,writestatusAPIKey);
               if(constatuscode2!=200)
                  {
               Serial.println("Error updating status to cloud. Error code: ");
               Serial.print(constatuscode2);
                  }
               else
                 {
                    digitalWrite(led3pin,HIGH);
                     delay(1000);
                    Serial.println("Dining room light is on");
                    flagled3=1;
                 }
      }
       else if(Controlcode==104) 
      {  
               constatuscode2=ThingSpeak.writeField( statusChannelNumber,statusfanFieldNumber,1,writestatusAPIKey);
               if(constatuscode2!=200)
                  {
               Serial.println("Error updating status to cloud. Error code: ");
               Serial.print(constatuscode2);
                  }
               else
                 {
                    for(int pos=0;pos<=180;pos+=10)
                    {
                      myservo.write(pos);
                      delay(10);
                    }
                    for(int pos=180;pos<=0;pos-=10)
                    {
                        myservo.write(pos);
                        delay(10);
                    }
                    Serial.println("Fan is on");
                    flagfan=1;
                    delay(1000);
                 }  
     }
       else if(Controlcode==106)
     {
               constatuscode2=ThingSpeak.writeField( statusChannelNumber,statusled1FieldNumber,0,writestatusAPIKey);
               if(constatuscode2!=200)
                  {
               Serial.println("Error updating status to cloud. Error code: ");
               Serial.print(constatuscode2);
                   }
               else
                 {
                    digitalWrite(led1pin,LOW);
                    delay(1000);
                    Serial.println("living room light is off");
                    flagled1=0;
                  }
     }   
        else if(Controlcode==107)
     {
               constatuscode2=ThingSpeak.writeField( statusChannelNumber,statusled2FieldNumber,0,writestatusAPIKey);
               if(constatuscode2!=200)
                  {
               Serial.println("Error updating status to cloud. Error code: ");
               Serial.print(constatuscode2);
                  }
               else
                 {
                    digitalWrite(led2pin,LOW);
                    delay(1000);
                    Serial.println("Bedroom light is off");
                    flagled2=0;
                 }  
      }
        else if(Controlcode==108)
      {
               constatuscode2=ThingSpeak.writeField( statusChannelNumber,statusled3FieldNumber,0,writestatusAPIKey);
               if(constatuscode2!=200)
                  {
               Serial.println("Error updating status to cloud. Error code: ");
               Serial.print(constatuscode2);
                  }
               else
                 {
                    digitalWrite(led3pin,LOW);
                    delay(1000);
                    Serial.println("Dining room light is off");
                    flagled3=0;
                 }
      }
        else if(Controlcode==109)
      {
               constatuscode2=ThingSpeak.writeField( statusChannelNumber,statusfanFieldNumber,0,writestatusAPIKey);
               if(constatuscode2!=200)
                  {
               Serial.println("Error updating status to cloud. Error code: ");
               Serial.print(constatuscode2);
                  }
               else
                 { 
                Serial.println("fan is off");
                flagfan=0;
                 }
     }
        else if(Controlcode==119)
     {
     
      for(int pos=110;pos<=160;pos+=1)
        {
         myservo1.write(pos);
         delay(50);
        }
     delay(5000);
     for(int pos=160;pos>=110;pos-=1)
        {
        myservo1.write(pos);  
        delay(50);
        }
      
   }
 else
{
   Serial.println("Problem reading channel. HTTP error code: " );
   Serial.print(String(constatusCode1)); 
}
 
 delay(5000); // No need to read the temperature too often.
}
