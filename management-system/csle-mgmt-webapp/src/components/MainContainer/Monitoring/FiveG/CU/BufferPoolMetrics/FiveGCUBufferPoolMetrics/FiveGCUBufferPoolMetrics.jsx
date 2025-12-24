import React from 'react'
import './FiveGCUBufferPoolMetrics.css'
import FiveGCUBufferPoolCacheSizeChart from '../FiveGCUBufferPoolCacheSizeChart/FiveGCUBufferPoolCacheSizeChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G CU app resource usage metrics
 */
const FiveGCUBufferPoolMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGCUBufferPoolMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGCUBufferPoolMetrics === null) {
      return (
        <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
          <span className="visually-hidden"></span>
        </Spinner>)
    } else {
      return (
        <div className="aggregatedMetrics">
          <div className="row chartsRow">
            <div className="col-sm-12 chartsCol">

              <h3 className="chartsTitle">CU central cache size</h3>
              <FiveGCUBufferPoolCacheSizeChart stats={props.fiveGCUBufferPoolMetrics}
                                               animation={props.animation} animationDuration={props.animationDuration}
                                               animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
        </div>
      )
    }
  }
)
FiveGCUBufferPoolMetrics.displayName = 'FiveGCUBufferPoolMetrics'
FiveGCUBufferPoolMetrics.propTypes = {}
FiveGCUBufferPoolMetrics.defaultProps = {}
export default FiveGCUBufferPoolMetrics
