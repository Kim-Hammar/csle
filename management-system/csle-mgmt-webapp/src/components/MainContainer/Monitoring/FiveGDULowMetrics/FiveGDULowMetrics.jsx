import React from 'react'
import './FiveGDULowMetrics.css'
import FiveGDULowLatencyChart from '../FiveGDULowLatencyChart/FiveGDULowLatencyChart.jsx'
import FiveGDULowCPUUsageChart from '../FiveGDULowCPUUsageChart/FiveGDULowCPUUsageChart.jsx'
import FiveGDULowSINRChart from '../FiveGDULowSINRChart/FiveGDULowSINRChart.jsx'
import FiveGDULowDecodingLatencyChart from '../FiveGDULowDecodingLatencyChart/FiveGDULowDecodingLatencyChart.jsx'
import FiveGDULowFECThroughputChart from '../FiveGDULowFECThroughputChart/FiveGDULowFECThroughputChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G DU Lowmetrics
 */
const FiveGDULowMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGDULowMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGDULowMetrics === null) {
      return (
        <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
          <span className="visually-hidden"></span>
        </Spinner>)
    } else {
      return (
        <div className="aggregatedMetrics">
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Physical layer processing latency</h3>
              <FiveGDULowLatencyChart stats={props.fiveGDULowMetrics}
                                      animation={props.animation} animationDuration={props.animationDuration}
                                      animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Physical layer CPU usage %</h3>
              <FiveGDULowCPUUsageChart stats={props.fiveGDULowMetrics}
                                       animation={props.animation} animationDuration={props.animationDuration}
                                       animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Uplink signal to noise ratio (dB)</h3>
              <FiveGDULowSINRChart stats={props.fiveGDULowMetrics}
                                   animation={props.animation} animationDuration={props.animationDuration}
                                   animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Channel estimation and decoding latency (ms)</h3>
              <FiveGDULowDecodingLatencyChart stats={props.fiveGDULowMetrics}
                                              animation={props.animation} animationDuration={props.animationDuration}
                                              animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-12 chartsCol">

              <h3 className="chartsTitle">Forward error correction throughput (mbps)</h3>
              <FiveGDULowFECThroughputChart stats={props.fiveGDULowMetrics}
                                   animation={props.animation} animationDuration={props.animationDuration}
                                   animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
        </div>
      )
    }
  }
)
FiveGDULowMetrics.displayName = 'FiveGDUMetrics'
FiveGDULowMetrics.propTypes = {}
FiveGDULowMetrics.defaultProps = {}
export default FiveGDULowMetrics
