import React from 'react'
import './FiveGDUCellMetrics.css'
import FiveGDUCellLatencyChart from '../FiveGDUCellLatencyChart/FiveGDUCellLatencyChart.jsx'
import FiveGDUCellActiveUEsChart from '../FiveGDUCellActiveUEsChart/FiveGDUCellActiveUEsChart.jsx'
import FiveGDUCellBitrateChart from '../FiveGDUCellBitrateChart/FiveGDUCellBitrateChart.jsx'
import FiveGDUCellMCSChart from '../FiveGDUCellMCSChart/FiveGDUCellMCSChart.jsx'
import FiveGDUCellPUSCHSNRChart from '../FiveGDUCellPUSCHSNRChart/FiveGDUCellPUSCHSNRChart.jsx'
import FiveGDUCellBlockErrorRateChart from '../FiveGDUCellBlockErrorRateChart/FiveGDUCellBlockErrorRateChart.jsx'
import FiveGDUCellChannelQualityIndicatorChart from '../FiveGDUCellChannelQualityIndicatorChart/FiveGDUCellChannelQualityIndicatorChart.jsx'
import Spinner from 'react-bootstrap/Spinner'

/**
 * Component containing plots of 5G DU Cell metrics
 */
const FiveGDUCellMetrics = React.memo((props) => {
    if (!props.loading && (props.fiveGDUCellMetrics === null)) {
      return (<></>)
    }
    if (props.loading || props.fiveGDUCellMetrics === null) {
      return (
        <Spinner animation="border" role="status" className="aggregatedMetricsSpinner">
          <span className="visually-hidden"></span>
        </Spinner>)
    } else {
      return (
        <div className="aggregatedMetrics">
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">DU cell scheduling processing latency (us)</h3>
              <FiveGDUCellLatencyChart stats={props.fiveGDUCellMetrics}
                                       animation={props.animation} animationDuration={props.animationDuration}
                                       animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">DU number of active UEs</h3>
              <FiveGDUCellActiveUEsChart stats={props.fiveGDUCellMetrics}
                                         animation={props.animation} animationDuration={props.animationDuration}
                                         animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">DU cell bitrate (bps)</h3>
              <FiveGDUCellBitrateChart stats={props.fiveGDUCellMetrics}
                                       animation={props.animation} animationDuration={props.animationDuration}
                                       animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">DU modulation and coding scheme (MCS)</h3>
              <FiveGDUCellMCSChart stats={props.fiveGDUCellMetrics}
                                   animation={props.animation} animationDuration={props.animationDuration}
                                   animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">DU Physical Uplink Shared Channel (PUSCH) and Physical Uplink Control Channel
                (PUCCH) SNR</h3>
              <FiveGDUCellPUSCHSNRChart stats={props.fiveGDUCellMetrics}
                                        animation={props.animation} animationDuration={props.animationDuration}
                                        animationDurationFactor={props.animationDurationFactor} />
            </div>
            <div className="col-sm-6 chartsCol">

              <h3 className="chartsTitle">DU block error rate</h3>
              <FiveGDUCellBlockErrorRateChart stats={props.fiveGDUCellMetrics}
                                              animation={props.animation} animationDuration={props.animationDuration}
                                              animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
          <div className="row chartsRow">
            <div className="col-sm-12 chartsCol">

              <h3 className="chartsTitle">DU channel quality indicator (CQI)</h3>
              <FiveGDUCellChannelQualityIndicatorChart stats={props.fiveGDUCellMetrics}
                                        animation={props.animation} animationDuration={props.animationDuration}
                                        animationDurationFactor={props.animationDurationFactor} />
            </div>
          </div>
        </div>
      )
    }
  }
)
FiveGDUCellMetrics.displayName = 'FiveGDUCellMetrics'
FiveGDUCellMetrics.propTypes = {}
FiveGDUCellMetrics.defaultProps = {}
export default FiveGDUCellMetrics
