mod fs {
    pub mod xci {
        pub struct Xci;
    }

    pub mod pxci {
        pub struct UXci;
        pub struct NXci;
        pub struct LXci;
    }

    pub mod nca {
        pub struct Nca;
    }

    pub mod nsp {
        pub struct Nsp;
    }

    pub mod rom {
        pub struct Rom;
    }

    pub mod nacp {
        pub struct Nacp;
    }

    pub mod pfs0 {
        pub struct Pfs0;
    }

    pub mod hfs0 {
        pub struct Hfs0;
    }

    pub mod ticket {
        pub struct Ticket;
    }

    pub mod file {
        pub struct File;
    }

    pub mod chrome_nsp {
        pub struct ChromeNsp;
    }

    pub mod chrome_xci {
        pub struct ChromeXci;
    }

    pub mod chrome_nacp {
        pub struct ChromeNacp;
    }
}

use fs::xci::Xci;
use fs::pxci::{UXci, NXci, LXci};
use fs::nca::Nca;
use fs::nsp::Nsp;
use fs::rom::Rom;
use fs::nacp::Nacp;
use fs::pfs0::Pfs0;
use fs::hfs0::Hfs0;
use fs::ticket::Ticket;
use fs::file::File;
use fs::chrome_nsp::ChromeNsp;
use fs::chrome_xci::ChromeXci;
use fs::chrome_nacp::ChromeNacp;

fn factory(name: &str) -> Box<dyn std::any::Any> {
    if name.ends_with(".xci") || name.ends_with(".xcz") {
        Box::new(Xci)
    } else if name.ends_with(".nsp") || name.ends_with(".nsz") || name.ends_with(".nsx") {
        Box::new(Nsp)
    } else if name.ends_with(".nca") {
        Box::new(Nca)
    } else if name.ends_with(".ncz") {
        Box::new(File)
    } else if name.ends_with(".nacp") {
        Box::new(Nacp)
    } else if name.ends_with(".tik") {
        Box::new(Ticket)
    } else if name.ends_with(".hfs0") {
        Box::new(Hfs0)
    } else {
        Box::new(File)
    }
}
