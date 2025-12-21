import React from 'react'
import './FiveGCUCPRequestsChart.css'
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
 * Component containing a plot showing the paging/handover requests/events at the 5G CU
 */
const FiveGCUCPRequestsChart = React.memo((props) => {
    const margin = {
      top: 10,
      right: 30,
      left: 15,
      bottom: 25
    }

    if (props.stats !== undefined && props.stats.length > 0) {
      const data = props.stats.map((cu_cp_metrics, index) => {
        return {
          't': (index + 1),
          'Number of paging requests': parseInt(cu_cp_metrics.nof_cn_initiated_paging_requests),
          'Number of handover preparations': parseInt(cu_cp_metrics.nof_handover_preparations_requested),
          'Number of successful handover preparations': parseInt(cu_cp_metrics.nof_successful_handover_preparations),
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
                <Label angle={270} value="Number of requests" offset={0} position="insideLeft"
                       className="largeFont"
                       dy={50} />
              </YAxis>
              <Tooltip />
              <Legend verticalAlign="top" wrapperStyle={{ position: 'relative', fontSize: '15px' }}
                      className="largeFont" />
              <Line isAnimationActive={props.animation} animation={props.animation} type="monotone"
                    dataKey="Number of paging requests"
                    stroke="#8884d8" addDot={false} activeDot={{ r: 8 }}
                    animationEasing={'linear'}
                    animationDuration={((1 - (props.animationDuration / 100)) * props.animationDurationFactor)} />
              <Line animation={props.animation} type="monotone" dataKey="Number of handover preparations"
                    stroke="#82ca9d" animationEasing={'linear'}
                    animationDuration={((1 - (props.animationDuration / 100)) * props.animationDurationFactor)}
                    isAnimationActive={props.animation}/>
              <Line animation={props.animation} type="monotone" dataKey="Number of successful handover preparations"
                    stroke="#8b0000" animationEasing={'linear'}
                    animationDuration={((1 - (props.animationDuration / 100)) * props.animationDurationFactor)}
                    isAnimationActive={props.animation}/>
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
FiveGCUCPRequestsChart.displayName = 'FiveGCUCPRequestsChart'
FiveGCUCPRequestsChart.propTypes = {}
FiveGCUCPRequestsChart.defaultProps = {}
export default FiveGCUCPRequestsChart
