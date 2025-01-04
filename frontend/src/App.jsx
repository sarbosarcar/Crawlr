
import './App.css'

import Navbar from './components/Navbar'
import Query from './components/Query'
import Response from './components/Response'
import Footer from './components/Footer'

function App() {

  return (
    <>
    <div className='w-full h-full bg-gray-800 p-8 font-mono'>
      <Navbar />
      <Query className='flex justify-center items-center' />
      <Response />
      <Footer className='my-32' />
    </div>
    </>
  )
}

export default App
