import React from 'react'
import './FiveGDURLCSDUErrorsChart.css'
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
 * Component containing a plot showing the error statistics of SDUs at the DU
 */
const FiveGDURLCSDUErrorsChart = React.memo((props) => {
    const margin = {
      top: 10,
      right: 30,
      left: 15,
      bottom: 25
    }

    if (props.stats !== undefined && props.stats !== null && props.stats.length > 0) {
      const data = props.stats.map((five_g_du_rlc_metrics, index) => {
        const totalSdus = Number(five_g_du_rlc_metrics.rx_num_sdus) || 0;
        const safeCalc = (numerator) => {
          if (totalSdus === 0) return 0;
          return (numerator / totalSdus);
        };
        return {
          't': (index + 1),
          'Dropped SDUs (%)': safeCalc(five_g_du_rlc_metrics.rx_num_dropped_sdus),
          'Discarded SDUs (%)': safeCalc(five_g_du_rlc_metrics.rx_num_discarded_sdus)
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
                <Label angle={270} value="Processing latency (ns)" offset={0} position="insideLeft"
                       className="largeFont"
                       dy={50} />
              </YAxis>
              <Tooltip />
              <Legend verticalAlign="top" wrapperStyle={{ position: 'relative', fontSize: '15px' }}
                      className="largeFont" />
              <Line isAnimationActive={props.animation} animation={props.animation} type="monotone"
                    dataKey="Dropped SDUs (%)"
                    stroke="#8884d8" addDot={false} activeDot={{ r: 8 }}
                    animationEasing={'linear'}
                    animationDuration={((1 - (props.animationDuration / 100)) * props.animationDurationFactor)} />
              <Line animation={props.animation} type="monotone" dataKey="Discarded SDUs (%)"
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
FiveGDURLCSDUErrorsChart.displayName = 'FiveGDURLCSDUErrorsChart'
FiveGDURLCSDUErrorsChart.propTypes = {}
FiveGDURLCSDUErrorsChart.defaultProps = {}
export default FiveGDURLCSDUErrorsChart
