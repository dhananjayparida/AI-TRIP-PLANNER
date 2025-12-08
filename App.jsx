import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from "axios"


function App() {
  const [count, setCount] = useState(0)

  async function showPlan() {
    try{
      const response=await axios.get("http://127.0.0.1:5000/Smart_Trip_Planner/bhubaneswar/jamshedpur/5/4500");
      console.log(response);
    }
    catch(err){
      console.log(err);
    }
    
  }
  showPlan();

  return (
    <>
    <button value="GET" onClick={()=>showPlan}></button>
      
    </>
  )
}

export default App
