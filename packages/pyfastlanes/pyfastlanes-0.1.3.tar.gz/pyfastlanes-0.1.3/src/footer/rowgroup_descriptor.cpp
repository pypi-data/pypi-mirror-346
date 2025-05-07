#include "fls/footer/rowgroup_descriptor.hpp"
#include "fls/cfg/cfg.hpp"
#include "fls/common/assert.hpp"
#include "fls/common/magic_enum.hpp"
#include "fls/io/file.hpp"
#include "fls/json/fls_json.hpp"
#include "fls/json/nlohmann/json.hpp"
#include "fls/table/rowgroup.hpp"

namespace fastlanes {
void RowgroupDescriptor::AddCol(const ColumnDescriptor& col) {
	/**/
	m_column_descriptors.push_back(col);
}

n_t RowgroupDescriptor::GetNextColIdx() const {
	/**/
	return static_cast<idx_t>(m_column_descriptors.size());
}

map RowgroupDescriptor::GetMap() const {
	/**/
	return m_name_idx_map;
}

idx_t RowgroupDescriptor::LookUp(const string& name) const {
	const auto it = m_name_idx_map.find(name);
	if (it == m_name_idx_map.end()) {
		throw std::runtime_error("name does not exist in the schema");
	}

	return it->second;
}

up<RowgroupDescriptor> RowgroupDescriptor::Project(const vector<idx_t>& idxs) const {
	auto footer = make_unique<RowgroupDescriptor>();

	idx_t new_idx {0};
	for (const auto idx : idxs) {
		if (idx >= m_column_descriptors.size()) {
			throw std::runtime_error("column index out of range");
		}
		// new description
		auto descriptor = m_column_descriptors[idx];
		descriptor.idx  = new_idx;
		footer->m_column_descriptors.push_back(descriptor);
		// new mapping
		footer->m_name_idx_map.emplace(m_column_descriptors[idx].name, new_idx);

		new_idx++;
	}

	return footer;
}

const_col_description_it RowgroupDescriptor::end() const {
	/**/
	return this->m_column_descriptors.end();
}

col_description_it RowgroupDescriptor::end() {
	/**/
	return this->m_column_descriptors.end();
}

const_col_description_it RowgroupDescriptor::begin() const {
	/**/
	return this->m_column_descriptors.begin();
}

col_description_it RowgroupDescriptor::begin() {
	/**/
	return this->m_column_descriptors.begin();
}

const ColumnDescriptor& RowgroupDescriptor::operator[](const n_t idx) const {
	FLS_ASSERT_L(idx, m_column_descriptors.size());

	return m_column_descriptors[idx];
}

RowgroupDescriptor::RowgroupDescriptor()
    : m_n_vec(0)
    , m_size {0}
    , m_n_tuples {0} {};

n_t GetNVector(const n_t n_tup) {
	return static_cast<n_t>(ceil(static_cast<double>(n_tup) / static_cast<double>(CFG::VEC_SZ)));
}

void RowgroupDescriptor::push_back(ColumnDescriptor&& scheme) {
	/**/
	m_column_descriptors.push_back(scheme);
}

vector<string> RowgroupDescriptor::GetColumnNames() const {
	vector<string> column_names;
	for (const auto& col_descriptor : m_column_descriptors) {
		column_names.push_back(col_descriptor.name);
	}

	return column_names;
}

vector<DataType> RowgroupDescriptor::GetDataTypes() const {
	vector<DataType> column_data_types;
	for (const auto& col_descriptor : m_column_descriptors) {
		column_data_types.push_back(col_descriptor.data_type);
	}

	return column_data_types;
}

n_t RowgroupDescriptor::GetNVectors() const {
	return m_n_vec;
}

void set_index(ColumnDescriptors& column_descriptors) {
	for (n_t col_idx = 0; col_idx < column_descriptors.size(); ++col_idx) {
		auto& column_descriptor = column_descriptors[col_idx];
		column_descriptor.idx   = col_idx;
		if (!column_descriptor.children.empty()) {
			set_index(column_descriptor.children);
		}
	}
}

up<RowgroupDescriptor> make_rowgroup_descriptor(const Rowgroup& rowgroup) {
	auto rowgroup_descriptor = make_unique<RowgroupDescriptor>(rowgroup.m_descriptor);

	// set the right col idx as it is ALWAYS not schema.json
	set_index(rowgroup_descriptor->m_column_descriptors);

	// set the num of vecs
	rowgroup_descriptor->m_n_vec    = rowgroup.VecCount();
	rowgroup_descriptor->m_n_tuples = rowgroup.n_tup;

	return rowgroup_descriptor;
}

up<RowgroupDescriptor> make_rowgroup_descriptor(const path& dir_path) {
	auto                 json_string     = File::read(dir_path);
	const nlohmann::json j               = nlohmann::json::parse(json_string);
	auto                 rowgroup_footer = j.get<RowgroupDescriptor>();
	return make_unique<RowgroupDescriptor>(rowgroup_footer);
}

ColumnDescriptor& RowgroupDescriptor::operator[](const n_t idx) {
	return m_column_descriptors[idx];
}

n_t RowgroupDescriptor::size() const {
	return m_column_descriptors.size();
}

} // namespace fastlanes
