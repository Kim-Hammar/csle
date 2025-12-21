import React from 'react'
import './FiveGDUAppResourceUsageMetrics.css'
import FiveGDUAppResourceUsageCPUChart from '../FiveGDUAppResourceUsageCPUChart/FiveGDUAppResourceUsageCPUChart.jsx'
import FiveGDUAppResourceUsageMemoryChart
  from '../FiveGDUAppResourceUsageMemoryChart/FiveGDUAppResourceUsageMemoryChart.jsx'
import FiveGDUAppResourceUsagePowerConsumptionChart
  from '../FiveGDUAppResourceUsagePowerConsumptionChart/FiveGDUAppResourceUsagePowerConsumptionChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G DU app resource usage metrics
 */
const FiveGDUAppResourceUsageMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGDUMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGDUMetrics === null) {
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
              <FiveGDUAppResourceUsageCPUChart stats={props.fiveGDUAppResourceUsageMetrics}
                                               animation={props.animation} animationDuration={props.animationDuration}
                                               animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">Application memory usage (mb)</h3>
              <FiveGDUAppResourceUsageMemoryChart stats={props.fiveGDUAppResourceUsageMetrics}
                                                  animation={props.animation} animationDuration={props.animationDuration}
                                                  animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-12 chartsCol">

              <h3 className="chartsTitle">Application power consumption (watts)</h3>
              <FiveGDUAppResourceUsagePowerConsumptionChart stats={props.fiveGDUAppResourceUsageMetrics}
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
FiveGDUAppResourceUsageMetrics.displayName = 'FiveGDUAppResourceUsageMetrics'
FiveGDUAppResourceUsageMetrics.propTypes = {}
FiveGDUAppResourceUsageMetrics.defaultProps = {}
export default FiveGDUAppResourceUsageMetrics
