#ifndef FLS_FOOTER_ROWGROUP_DESCRIPTOR_HPP
#define FLS_FOOTER_ROWGROUP_DESCRIPTOR_HPP

#include "fls/footer/column_descriptor.hpp"
#include "fls/std/filesystem.hpp"
#include "fls/std/unordered_map.hpp"

namespace fastlanes {
/*--------------------------------------------------------------------------------------------------------------------*/
class Rowgroup;
enum class DataType : uint8_t;
/*--------------------------------------------------------------------------------------------------------------------*/

using map                      = unordered_map<string, idx_t>;
using col_description_it       = vector<ColumnDescriptor>::iterator;
using const_col_description_it = vector<ColumnDescriptor>::const_iterator;

class RowgroupDescriptor {
public: /* Constructors */
	RowgroupDescriptor();
	RowgroupDescriptor(const RowgroupDescriptor&)              = default;
	RowgroupDescriptor(RowgroupDescriptor&&)                   = default;
	RowgroupDescriptor& operator=(const RowgroupDescriptor&) & = default;
	RowgroupDescriptor& operator=(RowgroupDescriptor&&) &      = default;
	~RowgroupDescriptor()                                      = default;

public:
	///
	[[nodiscard]] const ColumnDescriptors& GetColumnDescriptors() const {
		return m_column_descriptors;
	}
	///
	void AddCol(const ColumnDescriptor& col);
	///
	ColumnDescriptor& operator[](n_t idx);
	///
	const ColumnDescriptor& operator[](n_t idx) const;
	///
	[[nodiscard]] n_t GetNextColIdx() const;
	///
	[[nodiscard]] n_t size() const;
	///!
	[[nodiscard]] map GetMap() const;
	///
	col_description_it                     begin();
	[[nodiscard]] const_col_description_it begin() const;
	col_description_it                     end();
	[[nodiscard]] const_col_description_it end() const;
	///
	[[nodiscard]] idx_t LookUp(const string& name) const;
	///
	[[nodiscard]] up<RowgroupDescriptor> Project(const vector<idx_t>& idxs) const;
	///
	void push_back(ColumnDescriptor&&);
	//
	[[nodiscard]] vector<string> GetColumnNames() const;
	//
	[[nodiscard]] vector<DataType> GetDataTypes() const;
	//
	[[nodiscard]] n_t GetNVectors() const;

public:
	/// number of vectors
	n_t m_n_vec;
	///!
	ColumnDescriptors m_column_descriptors;
	///!
	map m_name_idx_map;
	// binary size of rowgroup
	sz_t m_size;
	//
	n_t m_offset;
	//
	n_t m_n_tuples;
};

up<RowgroupDescriptor> make_rowgroup_descriptor(const Rowgroup& rowgroup);
up<RowgroupDescriptor> make_rowgroup_descriptor(const path& dir_path);

} // namespace fastlanes

#endif // FLS_FOOTER_ROWGROUP_DESCRIPTOR_HPP
