import React from 'react'
import './FiveGDULowMetrics.css'
import FiveGDULowLatencyChart from '../FiveGDULowLatencyChart/FiveGDULowLatencyChart.jsx'
import FiveGDULowCPUUsageChart from '../FiveGDULowCPUUsageChart/FiveGDULowCPUUsageChart.jsx'
import FiveGDULowSINRChart from '../FiveGDULowSINRChart/FiveGDULowSINRChart.jsx'
import FiveGDULowDecodingLatencyChart from '../FiveGDULowDecodingLatencyChart/FiveGDULowDecodingLatencyChart.jsx'
import FiveGDULowFECThroughputChart from '../FiveGDULowFECThroughputChart/FiveGDULowFECThroughputChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G DU Low metrics
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

              <h3 className="chartsTitle">DU physical layer processing latency (us)</h3>
              <FiveGDULowLatencyChart stats={props.fiveGDULowMetrics}
                                      animation={props.animation} animationDuration={props.animationDuration}
                                      animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">DU physical layer CPU usage %</h3>
              <FiveGDULowCPUUsageChart stats={props.fiveGDULowMetrics}
                                       animation={props.animation} animationDuration={props.animationDuration}
                                       animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">DU uplink signal to noise ratio (dB)</h3>
              <FiveGDULowSINRChart stats={props.fiveGDULowMetrics}
                                   animation={props.animation} animationDuration={props.animationDuration}
                                   animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">DU channel estimation and decoding latency (us)</h3>
              <FiveGDULowDecodingLatencyChart stats={props.fiveGDULowMetrics}
                                              animation={props.animation} animationDuration={props.animationDuration}
                                              animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-12 chartsCol">

              <h3 className="chartsTitle">DU forward error correction throughput (mbps)</h3>
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
FiveGDULowMetrics.displayName = 'FiveGDULowMetrics'
FiveGDULowMetrics.propTypes = {}
FiveGDULowMetrics.defaultProps = {}
export default FiveGDULowMetrics
