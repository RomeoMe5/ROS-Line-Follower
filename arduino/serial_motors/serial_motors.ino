

// первый двигатель
#define ENA 11
#define IN1 13
#define IN2 12

// второй двигатель
#define ENB 10
#define IN3 8
#define IN4 9

struct Motor
{
  int in1;
  int in2;
  int en;  
};


Motor A;
Motor B;


void setupMotor(Motor *M, int in1, int in2, int en)
{
  *M = { in1 , in2 , en };
  pinMode(en, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  Serial.begin(9600);
}

void stopMotor(Motor *M)
{

  digitalWrite(M->in1, LOW);
  digitalWrite(M->in2, LOW);
}


void setMotorSpeed(Motor *M, int speed)
{
  
  if(speed > 0)
  {
    analogWrite(M->en, speed);
    digitalWrite(M->in1, HIGH);
    digitalWrite(M->in2, LOW);
  }
  else
  {
    analogWrite(M->en, -speed);
    digitalWrite(M->in1, LOW);
    digitalWrite(M->in2, HIGH);
  }
  

}

int sA, sB, tmpA, tmpB;
void setup()
{
  setupMotor(&A, IN1, IN2, ENA);
  setupMotor(&B, IN3, IN4, ENB);
}

void loop()
{

  if (Serial.available() > 0) 
  {
    int val = Serial.parseInt(); 
    if(val == 256)
    {
     tmpA = Serial.parseInt(); 
     tmpB = Serial.parseInt(); 
     if(tmpA != 256 && tmpB != 256)
     {
      sA = tmpA;
      sB = tmpB;
     }
    }
  }
  setMotorSpeed(&A, sA);
  setMotorSpeed(&B, sB);

}
