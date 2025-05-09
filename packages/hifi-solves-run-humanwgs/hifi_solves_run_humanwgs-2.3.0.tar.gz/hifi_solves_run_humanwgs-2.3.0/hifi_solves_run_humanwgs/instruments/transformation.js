(context) => {
  if (!context.samples) {
    throw new Error('Samples are required for this transformation');
  }
  if (context.workflow_params['HumanWGS_wrapper.family']?.samples?.length > 0) {
    return {}
  }

  return {
    workflow_params: {
      'HumanWGS_wrapper.family': {
        family_id: context.workflow_params['HumanWGS_wrapper.family']?.family_id ?? context.samples[0].id,
        samples: context.samples?.map(sample => {
          return {
            sample_id: sample.id,
            hifi_reads: sample.files.map(sampleFile => sampleFile.path),
            father_id: sample.father_id ?? "unknown",
            mother_id: sample.mother_id ?? "unknown",
            sex: sample.sex ?? "unknown",
            affected: sample.affected ?? false
          }
        }),
      },
    }
  }
}
