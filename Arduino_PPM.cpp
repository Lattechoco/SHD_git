#define CHANNEL_NUMBER 12  //set the number of chanels
#define CHANNEL_DEFAULT_VALUE 1500  //set the default servo value
#define FRAME_LENGTH 22500  //set the PPM frame length in microseconds (1ms = 1000µs)
#define PULSE_LENGTH 300  //set the pulse length

#define onState 1  //set polarity of the pulses: 1 is positive, 0 is negative
#define sigPin 10  //set PPM signal output pin on the arduino

int ppm[CHANNEL_NUMBER]; // PPM signal list
int VL[CHANNEL_NUMBER]; // value list

void setup(){  
  //initiallize default ppm values
  for(int i=0; i<CHANNEL_NUMBER; i++){
    if (i>4){
      ppm[i]= 1000;
      VL[i]= 1000;
    }
    else{
      ppm[i]= CHANNEL_DEFAULT_VALUE;
      VL[i]= CHANNEL_DEFAULT_VALUE;
    }
  }

  pinMode(sigPin, OUTPUT);
  digitalWrite(sigPin, !onState);  //set the PPM signal pin to the default state (off)
  
  cli();
  TCCR1A = 0; // set entire TCCR1 register to 0
  TCCR1B = 0;
  
  OCR1A = 100;  // compare match register, change this
  TCCR1B |= (1 << WGM12);  // turn on CTC mode
  TCCR1B |= (1 << CS11);  // 8 prescaler: 0,5 microseconds at 16mhz
  TIMSK1 |= (1 << OCIE1A); // enable timer compare interrupt
  sei();

}

void loop(){
  VL[0] = 1500; //Roll[A]
  VL[1] = 1500; //Pitch[E]
  VL[2] = 1500; //Throttle[T]
  VL[3] = 1800; //Yaw[R]

  ///!!!!!!!///
  VL[4] = 1000; //ARM
  ///WARNING!!!!!!///
  
  for(int j = 0; j<CHANNEL_NUMBER; j++)
  {
    ppm[j] = VL[j];
  }  
}


/// timer setting ///
ISR(TIMER1_COMPA_vect){  //leave this alone
  static boolean state = true;
  
  TCNT1 = 0;
  
  if (state) {  //start pulse
    digitalWrite(sigPin, onState);
    OCR1A = PULSE_LENGTH * 2;
    state = false;
  } else{  //end pulse and calculate when to start the next pulse
    static byte cur_chan_numb;
    static unsigned int calc_rest;
  
    digitalWrite(sigPin, !onState);
    state = true;

    if(cur_chan_numb >= CHANNEL_NUMBER){
      cur_chan_numb = 0;
      calc_rest = calc_rest + PULSE_LENGTH;// 
      OCR1A = (FRAME_LENGTH - calc_rest) * 2;
      calc_rest = 0;
    }
    else{
      OCR1A = (ppm[cur_chan_numb] - PULSE_LENGTH) * 2;
      calc_rest = calc_rest + ppm[cur_chan_numb];
      cur_chan_numb++;
    }     
  }
}