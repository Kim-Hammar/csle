import React from 'react'
import './FiveGCUAppResourceUsageMetrics.css'
import FiveGDUAppResourceUsageCPUChart from '../FiveGCUAppResourceUsageCPUChart/FiveGDUAppResourceUsageCPUChart.jsx'
import FiveGCUAppResourceUsageMemoryChart
  from '../FiveGCUAppResourceUsageMemoryChart/FiveGDUAppResourceUsageMemoryChart.jsx'
import FiveGCUAppResourceUsagePowerConsumptionChart
  from '../FiveGCUAppResourceUsagePowerConsumptionChart/FiveGDUAppResourceUsagePowerConsumptionChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G CU-CP metrics
 */
const FiveGCUAppResourceUsageMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGCUMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGCUMetrics === null) {
      return (
        <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
          <span className="visually-hidden"></span>
        </Spinner>)
    } else {
      return (
        <div className="aggregatedMetrics">
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Application CPU usage %</h3>
              <FiveGDUAppResourceUsageCPUChart stats={props.fiveGCUMetrics}
                                               animation={props.animation} animationDuration={props.animationDuration}
                                               animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Application memory usage (mb)</h3>
              <FiveGCUAppResourceUsageMemoryChart stats={props.fiveGCUMetrics}
                                                  animation={props.animation} animationDuration={props.animationDuration}
                                                  animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-12 chartsCol">

              <h3 className="chartsTitle">Application power consumption (watts)</h3>
              <FiveGCUAppResourceUsagePowerConsumptionChart stats={props.fiveGCUMetrics}
                                                            animation={props.animation}
                                                            animationDuration={props.animationDuration}
                                                            animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
        </div>
      )
    }
  }
)
FiveGCUAppResourceUsageMetrics.displayName = 'FiveGCUAppResourceUsageMetrics'
FiveGCUAppResourceUsageMetrics.propTypes = {}
FiveGCUAppResourceUsageMetrics.defaultProps = {}
export default FiveGCUAppResourceUsageMetrics
