#ifndef FLS_FOOTER_SEGMENT_DESCRIPTOR_HPP
#define FLS_FOOTER_SEGMENT_DESCRIPTOR_HPP

#include "fls/common/common.hpp"

namespace fastlanes {
/*--------------------------------------------------------------------------------------------------------------------*\
 * EntryPointType
\*--------------------------------------------------------------------------------------------------------------------*/
enum class EntryPointType : uint8_t {
	UINT8  = 0,
	UINT16 = 1,
	UINT32 = 2,
	UINT64 = 3,
};

constexpr size_t sizeof_entry_point_type(EntryPointType type) {
	switch (type) {
	case EntryPointType::UINT8:
		return 1;
	case EntryPointType::UINT16:
		return 2;
	case EntryPointType::UINT32:
		return 4;
	case EntryPointType::UINT64:
		return 8;
	default:
		return 0; // Handle unexpected values
	}
}

/*--------------------------------------------------------------------------------------------------------------------*\
 * SegmentDescriptor
\*--------------------------------------------------------------------------------------------------------------------*/
class SegmentDescriptor {
public:
	SegmentDescriptor();
	SegmentDescriptor(n_t entrypoint_offset, n_t entrypoint_size, n_t data_offset, n_t data_size);

public:
	n_t            entrypoint_offset;
	n_t            entrypoint_size;
	n_t            data_offset;
	n_t            data_size;
	EntryPointType entry_point_t;
};

} // namespace fastlanes
#endif // FLS_FOOTER_SEGMENT_DESCRIPTOR_HPP