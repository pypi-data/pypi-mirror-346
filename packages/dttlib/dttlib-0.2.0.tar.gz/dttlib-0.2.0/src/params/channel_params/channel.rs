use std::cmp::Ordering;
use std::hash::{Hash, Hasher};
use gps_pip::PipDuration;
use nds_cache_rs::buffer::Buffer;
#[cfg(any(feature = "python", feature = "python-pipe"))]
use pyo3::{
    pymethods,
    pyclass,
};
#[cfg(not(any(feature = "python", feature = "python-pipe")))]
use dtt_macros::{new, getter};
use super::{ChannelSettings, NDSDataType, ChannelType};

#[derive(Clone, Debug, Default)]
#[cfg_attr(any(feature = "python", feature = "python-pipe"), pyclass(eq, get_all))]
pub struct Channel {
    pub name: String,
    pub data_type: NDSDataType,
    pub channel_type: ChannelType,
    pub rate_hz: f64,
    pub dcu_id: Option<i64>,
    pub channel_number: Option<i64>,
    pub calibration: Option<i64>,
    pub heterodyne_freq_hz: Option<f64>,
    pub gain: Option<f64>,
    pub slope: Option<f64>,
    pub offset: Option<f64>,
    pub use_active_time: bool,
    pub units: Option<String>
}


/// Identification and calibration data for a channel
/// The sort of info we might expect from a data server channel list.
impl Hash for Channel {
    fn hash<H: Hasher>(&self, state: &mut H) {
        // channel name
        self.name.hash(state);

        // rate
        // get period in pips_per_sec
        let period_pips = PipDuration::freq_hz_to_period(self.rate_hz);
        period_pips.hash(state);

        // type
        self.data_type.hash(state);
    }
}

impl PartialEq<Self> for Channel {
    fn eq(&self, other: &Self) -> bool {
        (self.name == other.name)
            && (self.rate_hz == other.rate_hz)
            && (self.data_type == other.data_type)
    }
}

impl Eq for Channel {

}

impl From<Channel> for nds2_client_rs::Channel {
    fn from(value: Channel) -> Self {
        Self {
            name: value.name,
            channel_type: value.channel_type.into(),
            data_type: value.data_type.into(),
            sample_rate: value.rate_hz,
            gain: value.gain.unwrap_or(1.0) as f32,
            slope: value.slope.unwrap_or(1.0) as f32,
            offset: value.offset.unwrap_or(0.0) as f32,
            units: value.units.unwrap_or("".to_string()),
        }
    }
}

impl Into<nds_cache_rs::buffer::Channel> for Channel {
    fn into(self) -> nds_cache_rs::buffer::Channel {
        nds_cache_rs::buffer::Channel::new(
            self.name,
            nds_cache_rs::buffer::ChannelType::Raw,
            self.data_type.into(),
            self.rate_hz,
            self.gain.unwrap_or(1.0) as f32,
            self.slope.unwrap_or(1.0) as f32,
            self.offset.unwrap_or(0.0) as f32,
            self.units.unwrap_or(String::new()),
        )
    }
}

impl From<nds_cache_rs::buffer::Channel> for Channel {
    fn from(value: nds_cache_rs::buffer::Channel) -> Self {
        Self {
            name: value.name().to_owned(),
            data_type: value.data_type().into(),
            channel_type: value.channel_type().into(),
            rate_hz: value.sample_rate().into(),
            gain: Some(value.gain() as f64),
            offset: Some(value.offset() as  f64),
            slope: Some(value.slope() as f64),
            units: Some(value.units().to_owned()),
            ..Default::default()
        }
    }
}

impl From<&Buffer> for Channel {
    fn from(buffer: &Buffer) -> Self {
        buffer.channel().clone().into()
    }
}

impl From<ChannelSettings> for Channel {
    fn from(value: ChannelSettings) -> Self {
        value.channel
    }
}

impl PartialOrd for Channel {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        if self.name < other.name {
            Some(Ordering::Less)
        }
        else if self.name > other.name {
            Some(Ordering::Greater)
        }
        else if self.rate_hz < other.rate_hz {
            Some(Ordering::Less)
        }
        else if self.rate_hz > other.rate_hz {
            Some(Ordering::Greater)
        }
        else if self.data_type == other.data_type {
            Some(Ordering::Equal)
        }
        else {
            None
        }
    }
}

#[cfg_attr(any(feature = "python", feature = "python-pipe"), pymethods)]
impl Channel {
    #[new]
    pub fn new(name: String, data_type: NDSDataType, rate_hz: f64) -> Self {
        Channel {
            name,
            data_type,
            rate_hz,
            ..Default::default()
        }
    }
    
    ///
    #[getter]
    pub fn online(&self) -> bool {
        self.channel_type == ChannelType::Online || self.channel_type == ChannelType::TestPoint
    }
    
    #[getter]
    pub fn testpoint(&self) -> bool {
        self.channel_type == ChannelType::TestPoint
    }
}