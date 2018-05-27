#define echo1 6
#define trig1 7
#define echo2 5
#define trig2 4

#define bat_6v8 12
#define bat_6v2 13

#define pwm1  10
#define pwm2  11

long duracion, distancia;  
int duty=0; //100% = 255 -> 10% = 25.5 
int medio, bajo, c1, c2;
 
void setup() {                
  Serial.begin (9600);      // Puerto serial a 9600 baudios
  
  pinMode(echo1, INPUT);    // Pin 6 como entrada
  pinMode(echo2, INPUT);    // Pin 5 como entrada
  pinMode(trig1, OUTPUT);   // Pin 7 como salida  
  pinMode(trig2, OUTPUT);   // Pin 4 como salida  

  pinMode(bat_6v8, INPUT);  // Pin 12 como entrada
  pinMode(bat_6v2, INPUT);  // Pin 13 como entrada

  //pinMode(pwm1, OUTPUT);    // Pin 10 como salida  
  pinMode(pwm2, OUTPUT);    // Pin 11 como salida

  pinMode(9, INPUT);       // Pin 9 como entrada
  pinMode(8, INPUT);       // Pin 8 como entrada
  
  }
  
void loop() {
  analogWrite(pwm1,duty);
  analogWrite(pwm2,duty);

  medio=digitalRead(bat_6v8);
  bajo=digitalRead(bat_6v2);
  
  char L = Serial.read();
  if(L == 'z'){
    for(int i = 60; i <= 220; i += 5){ 
      analogWrite(pwm2,i);
      analogWrite(pwm1,i);
      //Serial.println(i);
      delay(1);
    }
    delay(200);
    analogWrite(pwm2,0);
    analogWrite(pwm1,0);
  }

  else if(L=='n'){
    for(int i = 60; i <= 220; i += 5){     
      analogWrite(pwm2,i);
      analogWrite(pwm1,i);
      delay(1);
    }
    delay(100);
    analogWrite(pwm2,0);
    analogWrite(pwm1,0);
  }
  
  else if(L=='x'){
    
    if (medio==1 && bajo==0){
      Serial.println("Nivel Medio");
    }
    else if (bajo==1){
      Serial.println("Nivel bajo");
    }
    else{
      Serial.println("Estado ok");
    }
  }

  else if(L == 'c'){
    
    digitalWrite(trig1, LOW);
    delayMicroseconds(2);
    digitalWrite(trig1, HIGH);   // genera el pulso de triger por 10ms
    delayMicroseconds(10);
    digitalWrite(trig1, LOW);
    
    duracion = pulseIn(echo1, HIGH);
    distancia = (duracion/2) / 29;    // calcula la distancia en centimetros

    Serial.print("Distancia1:");
    Serial.println(distancia);    // envia el valor de la distancia por el puerto serial
    delay(150);
  }

  else if(L == 'v'){
    
    digitalWrite(trig2, LOW);
    delayMicroseconds(2);
    digitalWrite(trig2, HIGH);   // genera el pulso de triger por 10ms
    delayMicroseconds(10);
    digitalWrite(trig2, LOW);
    
    duracion = pulseIn(echo2, HIGH);
    distancia = (duracion/2) / 29;    // calcula la distancia en centimetros

    Serial.print("Distancia2:");
    Serial.println(distancia);    // envia el valor de la distancia por el puerto serial  
  }
  //L=' ';
//////////////////////////////////////////////////////////////////////  
  /*
  c1=digitalRead(9);
  c2=digitalRead(8);
  
  if (c1==0 && c2==0){
    
  }
  else 
  
  if (c1==1 && c2==0){
    delay(750);
    duty+=25;
    if (duty >255){
      duty=250;
    }
    Serial.print("Duty:");
    Serial.println(duty);
  }
  else if (c1==0 && c2==1){
    delay(750);
    duty-=25;
    if (duty<150){
      duty=150;
    }
    Serial.print("Duty:");
    Serial.println(duty);
  }
  
  */
}
