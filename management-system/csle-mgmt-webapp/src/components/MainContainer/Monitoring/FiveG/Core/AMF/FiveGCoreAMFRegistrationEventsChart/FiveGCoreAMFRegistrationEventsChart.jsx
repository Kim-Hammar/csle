import React from 'react'
import './FiveGCoreAMFRegistrationEventsChart.css'
import {
  CartesianGrid,
  Label,
  Legend, Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts'


/**
 * Component containing a plot showing the registration events over time for the AMF service in the 5G Core
 */
const FiveGCoreAMFRegistrationEventsChart = React.memo((props) => {
    const margin = {
      top: 10,
      right: 30,
      left: 15,
      bottom: 25
    }

    if (props.stats !== undefined && props.stats.length > 0) {
      const data = props.stats.map((amf_metrics, index) => {
        return {
          't': (index + 1),
          'Registration requests': parseInt(amf_metrics.fivegs_amffunction_rm_reginitreq),
          'Successful registration requests': parseInt(amf_metrics.fivegs_amffunction_rm_reginitsucc)
        }
      })
      var domain = [0, Math.max(1, data.length)]
      return (
        <div style={{ height: 300 }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={data}
              margin={margin}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="t" type="number" domain={domain}>
                <Label value="Time-step t" offset={-20} position="insideBottom" className="largeFont" />
              </XAxis>
              <YAxis type="number">
                <Label angle={270} value="Number of events" offset={0} position="insideLeft"
                       className="largeFont"
                       dy={50} />
              </YAxis>
              <Tooltip />
              <Legend verticalAlign="top" wrapperStyle={{ position: 'relative', fontSize: '15px' }}
                      className="largeFont" />
              <Line isAnimationActive={props.animation} animation={props.animation} type="monotone"
                    dataKey="Registration requests"
                    stroke="#8884d8" addDot={false} activeDot={{ r: 8 }}
                    animationEasing={'linear'}
                    animationDuration={((1 - (props.animationDuration / 100)) * props.animationDurationFactor)} />
              <Line animation={props.animation} type="monotone" dataKey="Successful registration requests"
                    stroke="#8b0000" animationEasing={'linear'}
                    animationDuration={((1 - (props.animationDuration / 100)) * props.animationDurationFactor)}
                    isAnimationActive={props.animation} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )

    } else {
      return (
        <div></div>
      )
    }
  }
)
FiveGCoreAMFRegistrationEventsChart.displayName = 'FiveGCoreAMFRegistrationEventsChart'
FiveGCoreAMFRegistrationEventsChart.propTypes = {}
FiveGCoreAMFRegistrationEventsChart.defaultProps = {}
export default FiveGCoreAMFRegistrationEventsChart
