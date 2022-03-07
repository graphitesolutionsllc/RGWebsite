import React from 'react'

import { Helmet } from 'react-helmet'

import projectStyles from '../style.module.css'
import styles from './home.module.css'

const Home = (props) => {
  return (
    <div className={styles['container']}>
      <Helmet>
        <title>Stupendous Bustling Alligator</title>
        <meta property="og:title" content="Stupendous Bustling Alligator" />
      </Helmet>
      <div className={styles['container1']}></div>
      <form className={styles['form']}>
        <h1 className={styles['text']}>STORIS API</h1>
        <span className={styles['text1']}>
          <span>
            Welcome to the Ruby Gordon Employee Website, please continue
          </span>
          <br></br>
          <span>to log in to use features.</span>
        </span>
        <button className={` ${styles['button']} ${projectStyles['button']} `}>
          Log in
        </button>
      </form>
    </div>
  )
}

export default Home
