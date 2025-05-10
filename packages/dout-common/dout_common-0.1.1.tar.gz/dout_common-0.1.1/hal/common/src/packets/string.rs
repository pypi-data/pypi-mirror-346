use core::ops::{Deref, DerefMut};

use alloc::string::ToString;
use binrw::{BinRead, BinWrite};
use num_traits::AsPrimitive;

pub struct String<L: AsPrimitive<usize>>(alloc::string::String, core::marker::PhantomData<L>);

impl<L: AsPrimitive<usize>> Deref for String<L> {
    type Target = alloc::string::String;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}
impl<L: AsPrimitive<usize>> DerefMut for String<L> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}
impl<L: AsPrimitive<usize>> String<L> {
    pub fn to_string(self) -> alloc::string::String {
        self.0
    }
}

impl<L: AsPrimitive<usize>> From<alloc::string::String> for String<L> {
    fn from(s: alloc::string::String) -> Self {
        Self(s, core::marker::PhantomData)
    }
}

impl<L: AsPrimitive<usize>> core::fmt::Debug for String<L> {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        self.0.fmt(f)
    }
}

impl<L: AsPrimitive<usize>> BinRead for String<L> {
    type Args<'a> = (L,);

    fn read_options<R: binrw::io::Read + binrw::io::Seek>(
        reader: &mut R,
        _endian: binrw::Endian,
        args: Self::Args<'_>,
    ) -> binrw::BinResult<Self> {
        let mut data = alloc::vec![0u8; args.0.as_()];
        reader.read_exact(&mut data)?;
        alloc::string::String::from_utf8(data)
            .map(|v| Self(v, core::marker::PhantomData))
            .map_err(|_| binrw::Error::Custom {
                pos: 0,
                err: alloc::boxed::Box::new("Invalid UTF-8".to_string()),
            })
    }
}

impl<L: AsPrimitive<usize>> BinWrite for String<L> {
    type Args<'a> = ();

    fn write_options<W: binrw::io::Write>(
        &self,
        writer: &mut W,
        _endian: binrw::Endian,
        _args: Self::Args<'_>,
    ) -> binrw::BinResult<()> {
        writer.write_all(self.0.as_bytes())?;
        Ok(())
    }
}
