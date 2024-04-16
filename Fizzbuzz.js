
var result;
var n = prompt("Coloque o N°");
  
function FizzBuzz(n){
    if(isNaN(n)){
    alert("Please put one number")
    };
    if(n%5!=0 && n%3!=0){
      return result = n;
    };
    if(n%5==0 && n%3==0){
      return result = "FizzBuzz";
    };
    if(n%5!=0 && n%3==0){
      return result = "Buzz";
    };
    if(n%3!=0 && n%5==0){
      return result = "Fizz";
      
    };
  }; 
document.getElementById("result").innerText = `Seu resultado é ${FizzBuzz(n)}`  
